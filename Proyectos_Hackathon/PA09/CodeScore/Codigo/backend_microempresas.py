# ==========================
# Archivo: backend_microempresas.py 
# ==========================
# Backend para maneja datos, login y predicción.
import os
import json
import glob
import hashlib
import secrets
import datetime as dt
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import joblib
except Exception:
    # Si joblib no está disponible, el backend sigue funcionando pero sin cargar modelo.
    joblib = None


# ==========================
# CONFIG
# ==========================
# Rutas base del proyecto (CodeScore)
RAIZ = os.path.dirname(os.path.abspath(__file__))   # CodeScore/Codigo
PROJECT_DIR = os.path.dirname(RAIZ)                 # CodeScore

# Carpeta de datos persistentes
DATA_DIR = os.path.join(PROJECT_DIR, "Recursos", "data") # CodeScore/Recursos/data

# Carpeta donde vive el modelo ML (.joblib)
ARTIFACT_DIR = os.path.join(PROJECT_DIR, "Recursos", "artifacts") # CodeScore/Recursos/artifacts

# Carpetas donde se buscará el modelo (en orden)
ARTIFACTS_DIR_CANDIDATES = [
    ARTIFACT_DIR
]

# Archivos del sistema
EMPRESAS_CSV = os.path.join(DATA_DIR, "empresas.csv")
REGISTROS_CSV = os.path.join(DATA_DIR, "registros_15d.csv")
PREDICCIONES_CSV = os.path.join(DATA_DIR, "predicciones.csv")
CONFIG_JSON = os.path.join(DATA_DIR, "config.json")


DEFAULT_ADMIN_PASSWORD = "admin123"  # Cambiar luego en data/config.json (hash)


# ==========================
# UTIL: seguridad simple y manejo de archivos
# ==========================
# Devuelve el SHA256 en hexadecimal para un bloque de bytes.
def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

# Hashea la contraseña usando un salt (en hex) + SHA256.
def _hash_password(password: str, salt_hex: str) -> str:
    raw = bytes.fromhex(salt_hex) + password.encode("utf-8")
    return _sha256_hex(raw)

# Crea la carpeta si no existe (sin error si ya existe).
def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# Si el CSV no existe, lo crea vacío con las columnas indicadas.
def _ensure_csv(path: str, columns: List[str]):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

# Lee un CSV de forma segura; si falla, devuelve un DataFrame vacío.
def _read_csv_safe(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

# Guarda primero a un .tmp y luego reemplaza el archivo final.
def _write_csv_atomic(df: pd.DataFrame, path: str):
    '''
    Escritura atómica (sin .bak). Evita corrupción si se interrumpe guardado.
    '''
    folder = os.path.dirname(path)
    _ensure_dir(folder)
    tmp = path + ".tmp"
    df.to_csv(tmp, index=False)
    os.replace(tmp, path)

# Asegura que el CSV tenga las columnas requeridas (agrega las faltantes).
def _migrate_csv_schema(path: str, required_cols: List[str]):
    '''
    Si el CSV ya existe pero le faltan columnas nuevas, las agrega sin romper datos.
    '''
    if not os.path.exists(path):
        return
    df = _read_csv_safe(path)
    # Si está vacío, recrea el CSV solo con columnas requeridas.
    if df.empty:
        df2 = pd.DataFrame(columns=required_cols)
        _write_csv_atomic(df2, path)
        return
    changed = False
    for c in required_cols:
        if c not in df.columns:
            # Columna nueva se agrega con NaN para no romper datos existentes.
            df[c] = np.nan
            changed = True
    if changed:
        # Reordena columnas para que las requeridas queden al inicio.
        extra = [c for c in df.columns if c not in required_cols]
        df = df[required_cols + extra]
        _write_csv_atomic(df, path)


# ==========================
# MODELO ML
# ==========================
'''
Estructuras y funciones para cargar el modelo ML y su metadata.
'''
@dataclass
# Contenedor del modelo + info extra (features, clases, rutas).
class ModelBundle:
    model: object
    features: List[str]
    classes: List[str]
    model_path: str
    metadata_path: Optional[str] = None


# Cache global del modelo para no cargarlo múltiples veces.
_MODEL: Optional[ModelBundle] = None

# Busca el archivo .joblib más reciente en las carpetas candidatas.
def _find_latest_joblib() -> Optional[str]:
    candidates = []
    for d in ARTIFACTS_DIR_CANDIDATES:
        if not os.path.isdir(d):
            continue
        candidates += glob.glob(os.path.join(d, "*.joblib"))
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]

# Intenta encontrar un .json de metadata asociado al modelo.
def _find_metadata_for(model_path: str) -> Optional[str]:
    base = os.path.splitext(model_path)[0]
    direct = base + ".json"
    if os.path.exists(direct):
        return direct
    folder = os.path.dirname(model_path)
    js = glob.glob(os.path.join(folder, "*.json"))
    if js:
        js.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return js[0]
    return None

# Carga "features" y "classes" desde un JSON de metadata (si existe).
def _load_metadata_features(meta_path: str) -> Tuple[Optional[List[str]], Optional[List[str]]]:
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        features = meta.get("feature_columns") or meta.get("features") or meta.get("features_used")
        classes = meta.get("classes") or meta.get("class_labels")

        if features and isinstance(features, list):
            features = [str(x) for x in features]
        else:
            features = None

        if classes and isinstance(classes, list):
            classes = [str(x) for x in classes]
        else:
            classes = None

        return features, classes
    except Exception:
        return None, None

# Carga el modelo (y metadata) una sola vez y lo deja cacheado en _MODEL.
def load_model_bundle() -> Optional[ModelBundle]:
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    if joblib is None:
        return None

    model_path = _find_latest_joblib()
    if not model_path:
        return None

    try:
        mdl = joblib.load(model_path)
    except Exception:
        return None

    meta_path = _find_metadata_for(model_path)
    features = None
    classes = None
    # Si hay metadata, se intenta leer features/clases desde JSON.
    if meta_path:
        features, classes = _load_metadata_features(meta_path)

    if features is None:
        # Fallback para features desde scikit-learn (si el modelo expone feature_names_in_).
        try:
            if hasattr(mdl, "feature_names_in_"):
                features = list(mdl.feature_names_in_)
        except Exception:
            features = None

    if classes is None:
        # Fallback para clases desde scikit-learn (si el modelo expone classes_).
        try:
            if hasattr(mdl, "classes_"):
                classes = [str(x) for x in list(mdl.classes_)]
        except Exception:
            classes = ["BAJO", "MEDIO", "ALTO"]

    # Si no se detectan features, se usa una lista por defecto.
    if features is None:
        features = [
            "rubro",
            "anio",
            "mes",
            "ventas_15",            # facturado
            "ingresos_15",          # cobrado
            "tasa_cobro_15",
            "gastos_fijos_15",
            "gastos_variables_15",
            "gastos_totales_15",
            "activos_corrientes_15",
            "pasivos_corrientes_15",
            "margen_ganancia_15",
            "liquidez_corriente_15",
            "riesgo_15",
            "prob_riesgo_15",
        ]

    _MODEL = ModelBundle(
        model=mdl,
        features=features,
        classes=classes,
        model_path=model_path,
        metadata_path=meta_path,
    )
    return _MODEL


# ==========================
# INICIALIZACIÓN (CSV)
# ==========================
# Prepara carpetas/archivos CSV y config inicial para que el backend funcione.
def inicializar_backend():
    # Asegura que exista la carpeta data/.
    _ensure_dir(DATA_DIR)

    # Define columnas esperadas para cada CSV.
    empresas_cols = ["empresa_id", "nombre_empresa", "password_hash", "salt", "fecha_creacion"]
    registros_cols = [
        "empresa_id",
        "rubro",
        "anio",
        "mes",
        "mes_inicio",
        "ventas_15",               # FACTURADO
        "ingresos_15",             # COBRADO
        "tasa_cobro_15",           # ingresos/ventas
        "gastos_fijos_15",
        "gastos_variables_15",
        "gastos_totales_15",
        "activos_corrientes_15",
        "pasivos_corrientes_15",
        "margen_ganancia_15",
        "liquidez_corriente_15",
        "riesgo_15",
        "prob_riesgo_15",
        "fecha_guardado",
        "ultima_edicion",
    ]
    pred_cols = ["empresa_id", "anio", "mes", "riesgo_predicho", "prob_bajo", "prob_medio", "prob_alto", "timestamp"]

    # Crea los CSV si no existen.
    _ensure_csv(EMPRESAS_CSV, empresas_cols)
    _ensure_csv(REGISTROS_CSV, registros_cols)
    _ensure_csv(PREDICCIONES_CSV, pred_cols)

    # Migraciones (por si ya existían CSV sin la columna nueva)
    # Actualiza estructura de CSV antiguos agregando columnas faltantes.
    _migrate_csv_schema(EMPRESAS_CSV, empresas_cols)
    _migrate_csv_schema(REGISTROS_CSV, registros_cols)
    _migrate_csv_schema(PREDICCIONES_CSV, pred_cols)

    # Config admin
    # Si no existe config.json, lo crea con el hash del password admin.
    if not os.path.exists(CONFIG_JSON):
        salt = secrets.token_hex(16)
        ph = _hash_password(DEFAULT_ADMIN_PASSWORD, salt)
        cfg = {"admin_salt": salt, "admin_password_hash": ph}
        with open(CONFIG_JSON, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    # Intenta cargar el modelo al iniciar (si existe).
    load_model_bundle()


# ==========================
# EMPRESAS (LOGIN)
# ==========================
# CRUD básico de empresas + validación de inicio de sesión.
def crear_empresa(nombre_empresa: str, password: str) -> Tuple[bool, str]:
    nombre_empresa = (nombre_empresa or "").strip()
    password = password or ""
    # Valida datos y registra una nueva empresa en empresas.csv.
    if not nombre_empresa:
        return False, "El nombre de la empresa es obligatorio."
    if len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres."

    df = _read_csv_safe(EMPRESAS_CSV)
    if not df.empty and (df["nombre_empresa"].astype(str).str.lower() == nombre_empresa.lower()).any():
        return False, "Ya existe una empresa con ese nombre."

    # Genera ID y credenciales
    empresa_id = secrets.token_hex(8)
    salt = secrets.token_hex(16)
    ph = _hash_password(password, salt)

    # Crea la nueva fila y la guarda.
    nuevo = pd.DataFrame(
        [{
            "empresa_id": empresa_id,
            "nombre_empresa": nombre_empresa,
            "password_hash": ph,
            "salt": salt,
            "fecha_creacion": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }]
    )
    out = pd.concat([df, nuevo], ignore_index=True)
    _write_csv_atomic(out, EMPRESAS_CSV)
    return True, empresa_id

# Verifica si la empresa existe y si el hash del password coincide.
def validar_login(nombre_empresa: str, password: str) -> Tuple[bool, Optional[str], str]:
    nombre_empresa = (nombre_empresa or "").strip()
    password = password or ""
    df = _read_csv_safe(EMPRESAS_CSV)
    if df.empty:
        return False, None, "No hay empresas registradas. Cree una cuenta."

    mask = df["nombre_empresa"].astype(str).str.lower() == nombre_empresa.lower()
    if not mask.any():
        return False, None, "Empresa no encontrada."

    row = df[mask].iloc[0]
    salt = str(row["salt"])
    ph = str(row["password_hash"])
    if _hash_password(password, salt) != ph:
        return False, None, "Contraseña incorrecta."

    return True, str(row["empresa_id"]), "Inicio de sesión exitoso."

# Devuelve una tabla simple con empresa_id y nombre_empresa.
def listar_empresas() -> pd.DataFrame:
    df = _read_csv_safe(EMPRESAS_CSV)
    if df.empty:
        return pd.DataFrame(columns=["empresa_id", "nombre_empresa"])
    return df[["empresa_id", "nombre_empresa"]].copy()


# ==========================
# REGISTROS 15 DÍAS
# ==========================
# Funciones para guardar/leer registros financieros y calcular derivados.
def _calc_derivadas_15(d: Dict) -> Dict:
    """
    Ventas = FACTURADO (vendido, puede no haberse cobrado)
    Ingresos = COBRADO (dinero real que entró)
    tasa_cobro_15 = ingresos_15 / ventas_15
    """
    # Convierte valores a float o NaN si vienen vacíos/invalidos.
    def f(x):
        try:
            if x is None or x == "":
                return np.nan
            return float(x)
        except Exception:
            return np.nan

    # Lee variables base desde el payload.
    ventas = f(d.get("ventas_15"))              # FACTURADO
    ingresos = f(d.get("ingresos_15"))          # COBRADO
    gf = f(d.get("gastos_fijos_15"))
    gv = f(d.get("gastos_variables_15"))
    act = f(d.get("activos_corrientes_15"))
    pas = f(d.get("pasivos_corrientes_15"))

    # Gastos totales 
    # Suma gastos fijos + variables (si alguno existe).
    gastos_tot = np.nan
    if not np.isnan(gf) or not np.isnan(gv):
        gastos_tot = (0 if np.isnan(gf) else gf) + (0 if np.isnan(gv) else gv)

    # Margen (sobre cobrado)
    # Calcula margen usando ingresos como base (evita división entre cero).
    margen = np.nan
    if ingresos is not None and not np.isnan(ingresos):
        denom = ingresos if ingresos != 0 else 1e-9
        margen = ((0 if np.isnan(ingresos) else ingresos) - (0 if np.isnan(gastos_tot) else gastos_tot)) / denom

    # Liquidez
    # Activos corrientes / pasivos corrientes (evita división entre cero).
    liquidez = np.nan
    if act is not None and pas is not None and not np.isnan(act) and not np.isnan(pas):
        denom = pas if pas != 0 else 1e-9
        liquidez = act / denom

    # Ratio gastos/ingresos
    # Qué tan pesados son los gastos respecto a lo cobrado.
    ratio_gastos = np.nan
    if ingresos is not None and not np.isnan(ingresos) and ingresos != 0 and not np.isnan(gastos_tot):
        ratio_gastos = gastos_tot / ingresos

    # Tasa de cobro
    # Proporción de ventas que realmente se cobraron.
    tasa_cobro = np.nan
    if ventas is not None and not np.isnan(ventas) and ventas > 0 and ingresos is not None and not np.isnan(ingresos):
        tasa_cobro = ingresos / ventas

    # Riesgo_15 (informativo) incorporando tasa de cobro
    riesgo_15 = "MEDIO"
    prob_15 = 0.5

    utilidad = np.nan
    if ingresos is not None and not np.isnan(ingresos) and not np.isnan(gastos_tot):
        utilidad = ingresos - gastos_tot

    if (not np.isnan(tasa_cobro) and tasa_cobro < 0.60) or (not np.isnan(utilidad) and utilidad < 0) or (not np.isnan(ratio_gastos) and ratio_gastos >= 1.0):
        riesgo_15 = "ALTO"
        prob_15 = 0.85
    elif (not np.isnan(tasa_cobro) and tasa_cobro < 0.80) or (not np.isnan(ratio_gastos) and ratio_gastos >= 0.85):
        riesgo_15 = "MEDIO"
        prob_15 = 0.55
    else:
        riesgo_15 = "BAJO"
        prob_15 = 0.20

    # Devuelve el mismo dict con campos calculados listos para guardar.
    out = dict(d)
    out["ventas_15"] = ventas
    out["ingresos_15"] = ingresos
    out["tasa_cobro_15"] = tasa_cobro
    out["gastos_fijos_15"] = gf
    out["gastos_variables_15"] = gv
    out["gastos_totales_15"] = gastos_tot
    out["activos_corrientes_15"] = act
    out["pasivos_corrientes_15"] = pas
    out["margen_ganancia_15"] = margen
    out["liquidez_corriente_15"] = liquidez
    out["riesgo_15"] = riesgo_15
    out["prob_riesgo_15"] = prob_15
    return out

 # Crea o actualiza el registro de un mes para una empresa (upsert).
def upsert_registro_15d(
    empresa_id: str,
    anio: int,
    mes: int,
    rubro: str,
    payload_15: Dict,
) -> Tuple[bool, str]:
   
    if not empresa_id:
        return False, "Empresa inválida."
    try:
        anio = int(anio)
        mes = int(mes)
    except Exception:
        return False, "Año o mes inválido."
    if mes < 1 or mes > 12:
        return False, "Mes inválido (1-12)."

    # Normaliza rubro si viene vacío.
    rubro = (rubro or "General").strip() or "General"

    # Arma el dict base que se guardará.
    d = dict(payload_15)
    d["empresa_id"] = empresa_id
    d["anio"] = anio
    d["mes"] = mes
    d["rubro"] = rubro
    d["mes_inicio"] = f"{anio:04d}-{mes:02d}-01"

    # Calcula métricas derivadas antes de guardar.
    d = _calc_derivadas_15(d)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d["ultima_edicion"] = now

    df = _read_csv_safe(REGISTROS_CSV)

    # Si aún no hay registros, crea el CSV con la primera fila.
    if df.empty:
        d["fecha_guardado"] = now
        out = pd.DataFrame([d])
        _write_csv_atomic(out, REGISTROS_CSV)
        return True, "Registro creado."

    # Fuerza anio/mes como enteros para comparar bien.
    for col in ["anio", "mes"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Busca si ya existe registro para empresa + año + mes.
    mask = (
        (df["empresa_id"].astype(str) == str(empresa_id))
        & (df["anio"].astype("Int64") == anio)
        & (df["mes"].astype("Int64") == mes)
    )

    # Si existe, actualiza columnas (agrega nuevas si faltan).
    if mask.any():
        for k, v in d.items():
            if k not in df.columns:
                df[k] = np.nan
            df.loc[mask, k] = v
        _write_csv_atomic(df, REGISTROS_CSV)
        return True, "Registro actualizado."
    # Si no existe, agrega una nueva fila.
    else:
        d["fecha_guardado"] = now
        out = pd.concat([df, pd.DataFrame([d])], ignore_index=True)
        _write_csv_atomic(out, REGISTROS_CSV)
        return True, "Registro creado."

# Obtiene el registro de una empresa para un año/mes específico.
def obtener_registro_15d(empresa_id: str, anio: int, mes: int) -> Optional[Dict]:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return None
    try:
        anio = int(anio)
        mes = int(mes)
    except Exception:
        return None

    m = (
        (df["empresa_id"].astype(str) == str(empresa_id))
        & (pd.to_numeric(df["anio"], errors="coerce") == anio)
        & (pd.to_numeric(df["mes"], errors="coerce") == mes)
    )
    if not m.any():
        return None
    return df[m].iloc[0].to_dict()

# Lista los años disponibles que tienen registros para esa empresa.
def listar_anios_con_registros(empresa_id: str) -> List[int]:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return []
    d = df[df["empresa_id"].astype(str) == str(empresa_id)]
    if d.empty:
        return []
    return sorted(pd.to_numeric(d["anio"], errors="coerce").dropna().astype(int).unique().tolist())

# Lista los meses con registros para una empresa en un año dado.
def listar_meses_con_registros(empresa_id: str, anio: int) -> List[int]:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return []
    try:
        anio = int(anio)
    except Exception:
        return []
    d = df[
        (df["empresa_id"].astype(str) == str(empresa_id))
        & (pd.to_numeric(df["anio"], errors="coerce") == anio)
    ]
    if d.empty:
        return []
    return sorted(pd.to_numeric(d["mes"], errors="coerce").dropna().astype(int).unique().tolist())

# Devuelve todos los registros del año para esa empresa (ordenado por mes).
def obtener_tabla_anio(empresa_id: str, anio: int) -> pd.DataFrame:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return pd.DataFrame()
    try:
        anio = int(anio)
    except Exception:
        return pd.DataFrame()

    d = df[
        (df["empresa_id"].astype(str) == str(empresa_id))
        & (pd.to_numeric(df["anio"], errors="coerce") == anio)
    ].copy()
    if d.empty:
        return d
    d["mes"] = pd.to_numeric(d["mes"], errors="coerce").astype(int)
    return d.sort_values("mes")

# Elimina un registro específico (empresa + año + mes).
def eliminar_registro(empresa_id: str, anio: int, mes: int) -> Tuple[bool, str]:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return False, "No hay registros."
    try:
        anio = int(anio)
        mes = int(mes)
    except Exception:
        return False, "Año/mes inválido."

    mask = (
        (df["empresa_id"].astype(str) == str(empresa_id))
        & (pd.to_numeric(df["anio"], errors="coerce") == anio)
        & (pd.to_numeric(df["mes"], errors="coerce") == mes)
    )
    if not mask.any():
        return False, "Registro no encontrado."

    df2 = df.loc[~mask].copy()
    _write_csv_atomic(df2, REGISTROS_CSV)
    return True, "Registro eliminado."

# Elimina todos los registros de un año para una empresa.
def eliminar_anio(empresa_id: str, anio: int) -> Tuple[bool, str]:
    df = _read_csv_safe(REGISTROS_CSV)
    if df.empty:
        return False, "No hay registros."
    try:
        anio = int(anio)
    except Exception:
        return False, "Año inválido."

    mask = (df["empresa_id"].astype(str) == str(empresa_id)) & (pd.to_numeric(df["anio"], errors="coerce") == anio)
    if not mask.any():
        return False, "No hay registros para ese año."

    df2 = df.loc[~mask].copy()
    _write_csv_atomic(df2, REGISTROS_CSV)
    return True, "Año eliminado (todos los meses)."

# Elimina la empresa y también sus registros y predicciones asociadas.
def eliminar_empresa(empresa_id: str) -> Tuple[bool, str]:
    df_emp = _read_csv_safe(EMPRESAS_CSV)
    if df_emp.empty:
        return False, "No hay empresas."
    mask = df_emp["empresa_id"].astype(str) == str(empresa_id)
    if not mask.any():
        return False, "Empresa no encontrada."
    df_emp2 = df_emp.loc[~mask].copy()
    _write_csv_atomic(df_emp2, EMPRESAS_CSV)

    df_reg = _read_csv_safe(REGISTROS_CSV)
    if not df_reg.empty:
        df_reg2 = df_reg[df_reg["empresa_id"].astype(str) != str(empresa_id)].copy()
        _write_csv_atomic(df_reg2, REGISTROS_CSV)

    df_pred = _read_csv_safe(PREDICCIONES_CSV)
    if not df_pred.empty:
        df_pred2 = df_pred[df_pred["empresa_id"].astype(str) != str(empresa_id)].copy()
        _write_csv_atomic(df_pred2, PREDICCIONES_CSV)

    return True, "Empresa eliminada."


# ==========================
# ADMIN PASSWORD
# ==========================
# Validación del password del admin usando el config.json.
def validar_password_admin(password: str) -> bool:
    # Lee config.json y compara el hash del password ingresado.
    try:
        with open(CONFIG_JSON, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        salt = cfg.get("admin_salt", "")
        ph = cfg.get("admin_password_hash", "")
        if not salt or not ph:
            return False
        return _hash_password(password or "", salt) == ph
    except Exception:
        return False


# ==========================
# PREDICCIÓN (fin de mes)
# ==========================
# Genera la predicción de riesgo usando el modelo y guarda el resultado en predicciones.csv.
def predecir_riesgo_fin_mes(empresa_id: str, anio: int, mes: int) -> Tuple[bool, Dict, str]:
    # Carga el modelo (si no existe, devuelve error).
    mb = load_model_bundle()
    if mb is None:
        return False, {}, "No se encontró un modelo .joblib. Coloque el modelo en la carpeta artifacts/."

    # Obtiene el registro del mes (si no existe, no se puede predecir).
    row = obtener_registro_15d(empresa_id, anio, mes)
    if not row:
        return False, {}, "No existe registro para ese año/mes."

    # Construye el input X usando las features esperadas por el modelo.
    X = {}
    for c in mb.features:
        if c in row:
            X[c] = row[c]
        else:
            if c == "anio":
                X[c] = int(anio)
            elif c == "mes":
                X[c] = int(mes)
            elif c == "rubro":
                X[c] = row.get("rubro", "General")
            else:
                X[c] = np.nan

    Xdf = pd.DataFrame([X])

    # Ejecuta predicción de clase.
    try:
        pred = mb.model.predict(Xdf)[0]
    except Exception as ex:
        return False, {}, f"Error al predecir: {ex}"

    # Intenta sacar probabilidades por clase si el modelo soporta predict_proba.
    prob_map = {cl: None for cl in mb.classes}
    try:
        if hasattr(mb.model, "predict_proba"):
            proba = mb.model.predict_proba(Xdf)[0]
            cls = mb.classes
            try:
                if hasattr(mb.model, "classes_"):
                    cls = [str(x) for x in list(mb.model.classes_)]
            except Exception:
                pass
            for i, cl in enumerate(cls):
                if i < len(proba):
                    prob_map[str(cl)] = float(proba[i])
    except Exception:
        pass

    pb = prob_map.get("BAJO")
    pm = prob_map.get("MEDIO")
    pa = prob_map.get("ALTO")

    # Prepara el resultado final que se devuelve a la UI.
    res = {
        "riesgo_predicho": str(pred),
        "probabilidades": prob_map,
        "prob_bajo": pb,
        "prob_medio": pm,
        "prob_alto": pa,
        "model_path": mb.model_path,
        "metadata_path": mb.metadata_path,
        "features": mb.features,
    }

    # Guarda la predicción (si existe para ese mes, la actualiza).
    dfp = _read_csv_safe(PREDICCIONES_CSV)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = {
        "empresa_id": empresa_id,
        "anio": int(anio),
        "mes": int(mes),
        "riesgo_predicho": res["riesgo_predicho"],
        "prob_bajo": pb if pb is not None else np.nan,
        "prob_medio": pm if pm is not None else np.nan,
        "prob_alto": pa if pa is not None else np.nan,
        "timestamp": now,
    }

    # Si aún no hay predicciones, crea el CSV con la primera fila.
    if dfp.empty:
        out = pd.DataFrame([new_row])
    # Busca si ya existe predicción para empresa + año + mes.
    else:
        mask = (
            (dfp["empresa_id"].astype(str) == str(empresa_id))
            & (pd.to_numeric(dfp["anio"], errors="coerce") == int(anio))
            & (pd.to_numeric(dfp["mes"], errors="coerce") == int(mes))
        )
        if mask.any():
            # Actualiza la fila existente.
            for k, v in new_row.items():
                if k not in dfp.columns:
                    dfp[k] = np.nan
                dfp.loc[mask, k] = v
            out = dfp
        else:
            # Agrega una nueva fila de predicción.
            out = pd.concat([dfp, pd.DataFrame([new_row])], ignore_index=True)

    _write_csv_atomic(out, PREDICCIONES_CSV)
    return True, res, "Predicción generada."