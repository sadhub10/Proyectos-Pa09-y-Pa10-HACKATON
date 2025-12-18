# ==========================
# Archivo: main.py
# ==========================
# Interfaz principal (Flet): login/registro, registro de 15 días, predicciones y administración.
import os
import math
import pandas as pd
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from matplotlib.figure import Figure

import backend_microempresas as bf

# Color principal usado en la UI.
AZUL = "#1565C0"

# Catálogo de meses y años disponibles en los dropdowns.
MESES = [
    (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
    (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
    (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre"),
]
ANIOS = list(range(2015, 2026))


# ==========================
# FORMATOS / HELPERS
# ==========================
# Funciones para formatear números para mostrar en pantalla.
def fmt_money(x):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "-"
        return f"${float(x):,.2f}"
    except Exception:
        return "-"


def fmt_num(x, nd=3):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "-"
        return f"{float(x):.{nd}f}"
    except Exception:
        return "-"


def fmt_pct(x, nd=1):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "-"
        return f"{float(x)*100:.{nd}f}%"
    except Exception:
        return "-"

# Convierte los números del 1 al 12 a el nombre del mes (para tablas y dropdowns).
def mes_nombre(m):
    for k, n in MESES:
        if int(m) == int(k):
            return n
    return str(m)


def make_card(title: str, value: str, subtitle: str = ""):
    # Tarjeta reusable para métricas/resúmenes en la pestaña de predicciones.
    return ft.Card(
        content=ft.Container(
            padding=14,
            bgcolor="white",
            content=ft.Column(
                [
                    ft.Text(title, size=12, color="black"),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=AZUL),
                    ft.Text(subtitle, size=11, color="grey") if subtitle else ft.Container(height=0),
                ],
                spacing=4,
            ),
        )
    )


# ==========================
# GRÁFICAS (Matplotlib)
# ==========================
# Figuras que se renderizan dentro de Flet usando MatplotlibChart.
def fig_barras_finanzas_15(reg: dict) -> Figure:
    '''
    Barras mostrando diferencia entre 
    facturado y cobrado + gastos.
    '''
    fig = Figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)

    labels = ["Ventas fact.", "Ingresos cob.", "Gastos fijos", "Gastos var.", "Gastos tot."]
    vals = [
        float(reg.get("ventas_15", 0) or 0),
        float(reg.get("ingresos_15", 0) or 0),
        float(reg.get("gastos_fijos_15", 0) or 0),
        float(reg.get("gastos_variables_15", 0) or 0),
        float(reg.get("gastos_totales_15", 0) or 0),
    ]
    ax.bar(labels, vals)
    ax.set_title("Resumen financiero (primeros 15 días)")
    ax.set_ylabel("Monto (USD)")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    return fig

# Grafica las probabilidades BAJO/MEDIO/ALTO del modelo de fin de mes.
def fig_probabilidades(probs: dict) -> Figure:
    fig = Figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)
    order = ["BAJO", "MEDIO", "ALTO"]
    vals = []
    for k in order:
        v = probs.get(k)
        vals.append(0.0 if v is None or (isinstance(v, float) and math.isnan(v)) else float(v))
    ax.bar(order, vals)
    ax.set_ylim(0, 1)
    ax.set_title("Probabilidades por nivel de riesgo (fin de mes)")
    ax.set_ylabel("Probabilidad")
    fig.tight_layout()
    return fig


# Simula una curva tomando en cuenta los días 1..30 con base en la tendencia de 15 días y un factor por riesgo.
def fig_proyeccion_ganancia(reg: dict, riesgo: str) -> Figure:
    '''
    Proyección (simulación) de ganancia acumulada:
    - usa utilidad sobre COBRADO (ingresos_15 - gastos_totales_15)
    - ajusta según riesgo
    '''
    fig = Figure(figsize=(8, 4.5))
    ax = fig.add_subplot(111)

    ingresos_15 = float(reg.get("ingresos_15") or 0)  # cobrado
    gastos_15 = float(reg.get("gastos_totales_15") or 0)

    util_15 = ingresos_15 - gastos_15
    util_30_base = util_15 * 2

    r = str(riesgo).upper()
    if r == "ALTO":
        factor = 0.45
    elif r == "MEDIO":
        factor = 0.75
    else:
        factor = 1.05

    util_30_proj = util_30_base * factor

    dias_1_15 = list(range(1, 16))
    dias_16_30 = list(range(16, 31))

    y1 = [util_15 * (d / 15.0) for d in dias_1_15]
    y2 = []
    for d in dias_16_30:
        t = (d - 15) / 15.0
        y2.append(util_15 + t * (util_30_proj - util_15))

    dias = dias_1_15 + dias_16_30
    y = y1 + y2

    ax.plot(dias, y)
    ax.axhline(0, linewidth=1)

    ax.set_title("Proyección de ganancia acumulada (simulación)")
    ax.set_xlabel("Día del mes")
    ax.set_ylabel("Ganancia acumulada (USD)")
    fig.tight_layout()
    return fig


# ==========================
# MENSAJES (Advertencias/Recomendaciones)
# ==========================
# Texto dinámico según métricas y riesgo final estimado.
def generar_advertencia(reg: dict, riesgo: str) -> str:
    
    r = str(riesgo).upper()

    tc = reg.get("tasa_cobro_15")
    tc_low = False
    try:
        if tc is not None and not (isinstance(tc, float) and math.isnan(tc)) and float(tc) < 0.70:
            tc_low = True
    except Exception:
        pass

    if r == "ALTO":
        msg = (
            "Advertencia: si se mantiene el ritmo actual de cobros y gastos, "
            "el cierre del mes tendería a números negativos. Se recomienda aplicar medidas inmediatas: "
            "reducir gastos, renegociar fijos y acelerar cobros/ventas."
        )
        if tc_low:
            msg += " Además, la tasa de cobro es baja: se está vendiendo (fiado) pero no se está cobrando a tiempo."
        return msg

    if r == "MEDIO":
        msg = (
            "Advertencia: con el comportamiento actual, el cierre del mes podría quedar cerca de cero "
            "o volverse negativo. Se recomienda controlar gastos variables y reforzar ventas/cobranza "
            "en los próximos 15 días."
        )
        if tc_low:
            msg += " La tasa de cobro está por debajo de lo recomendado: refuerce cobranza y controle el fiado."
        return msg

    msg = (
        "Estado favorable: el cierre del mes luce estable si se mantiene el control actual. "
        "Continúe registrando y monitoreando sus indicadores."
    )
    if tc_low:
        msg += " Nota: aunque el riesgo sea bajo, la tasa de cobro es mejorable; cuide la cobranza."
    return msg

# Lista de acciones recomendadas basadas en reglas simples (heurística).
def generar_recomendaciones(reg: dict, riesgo: str) -> list[str]:
    rec = []
    ingresos = float(reg.get("ingresos_15") or 0)          # cobrado
    ventas = float(reg.get("ventas_15") or 0)              # facturado
    gastos_tot = float(reg.get("gastos_totales_15") or 0)
    gf = float(reg.get("gastos_fijos_15") or 0)
    gv = float(reg.get("gastos_variables_15") or 0)
    margen = reg.get("margen_ganancia_15")
    liq = reg.get("liquidez_corriente_15")
    tc = reg.get("tasa_cobro_15")

    ratio = None
    if ingresos > 0:
        ratio = gastos_tot / ingresos

    r = str(riesgo).upper()
    if r == "ALTO":
        rec.append("Aplique recorte de gastos variables y revise contratos de gastos fijos inmediatamente.")
        rec.append("Acelere cobranza: priorice clientes morosos, establezca fechas límite y reduzca el fiado.")
    elif r == "MEDIO":
        rec.append("Controle gastos diarios y establezca un presupuesto semanal.")
        rec.append("Refuerce cobranza y controle el fiado para no escalar a riesgo alto.")
    else:
        rec.append("Mantenga el control actual y documente sus decisiones financieras.")
        rec.append("Evalúe oportunidades de crecimiento sin aumentar gastos innecesarios.")

    # Regla fuerte por tasa de cobro
    try:
        if tc is not None and not (isinstance(tc, float) and math.isnan(tc)) and float(tc) < 0.75:
            rec.append("La tasa de cobro es baja. Refuerce cobranza y defina políticas de crédito (plazos, límites y penalizaciones).")
            if ventas > ingresos:
                rec.append("Existe diferencia entre facturado y cobrado. Revise cuentas por cobrar y acuerdos de pago.")
    except Exception:
        pass

    if ingresos <= 0 and ventas > 0:
        rec.append("Se está facturando pero casi no se está cobrando. Priorice estrategias de cobro y reduzca ventas a crédito.")
    if ingresos <= 0 and ventas <= 0:
        rec.append("Los ingresos y ventas facturadas son muy bajas o nulas. Revise el canal de ventas y estrategia comercial.")

    if ratio is not None and ratio >= 1.0:
        rec.append("Los gastos totales igualan o superan ingresos cobrados. Reduzca costos y evite gastos no esenciales.")
    elif ratio is not None and ratio >= 0.85:
        rec.append("Los gastos totales están altos respecto a ingresos cobrados. Ajuste presupuesto y reduzca consumo operativo.")

    if liq is not None:
        try:
            liqv = float(liq)
            if liqv < 1.0:
                rec.append("Liquidez por debajo de 1.0. Mejore cobranza, reduzca inventario o reprograme pagos.")
        except Exception:
            pass

    if margen is not None:
        try:
            marg = float(margen)
            if marg < 0.1 and r != "BAJO":
                rec.append("Margen bajo (sobre cobrado). Revise precios, costos unitarios y descuentos.")
        except Exception:
            pass

    if gf > gv and r != "BAJO":
        rec.append("Gastos fijos altos. Revise alquiler, planilla, servicios y renegocie si es posible.")
    if gv > 0 and ingresos > 0 and (gv / ingresos) > 0.5:
        rec.append("Gastos variables altos. Controle compras, logística y gastos operativos diarios.")

    return rec


# ==========================
# APP (Flet)
# ==========================
# Define pantallas, estado y eventos (login, tabs, acciones).
def main(page: ft.Page): # Config general de la ventana.
    page.title = "Riesgo Financiero — Microempresas"
    page.bgcolor = "white"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "start"
    page.scroll = ft.ScrollMode.AUTO

    # Inicializa backend (CSVs, config y modelo).
    bf.inicializar_backend()

    # SnackBar para mensajes rápidos (éxito/error).
    snackbar = ft.SnackBar(content=ft.Text(""), open=False)

    # Estado global simple (sesión actual).
    state = {"empresa_id": None, "empresa_nombre": None, "admin_unlocked": False}

    # Muestra un mensaje emergente en la UI.
    def set_snack(msg: str, error: bool = False):
        snackbar.content = ft.Text(msg)
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()

    # ==========================
    # HEADER (logueado)
    # ==========================
    # Barra superior cuando el usuario está dentro de la app.
    def build_header():
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Row(
                [
                    ft.Row( 
                        [
                            ft.Image(src="logo.png", width=70, height=70, fit=ft.ImageFit.CONTAIN),  #LOGO_PATH
                            ft.Column(
                                [
                                    ft.Text("MicroFinRisk", size=22, weight=ft.FontWeight.BOLD, color=AZUL),
                                    ft.Text("Predicción temprana de riesgo de cierre mensual", size=12, color="black"),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Text(f"Empresa: {state['empresa_nombre']}", size=12, color="black"),
                            ft.ElevatedButton("Cerrar sesión", bgcolor=AZUL, color="white", on_click=lambda e: mostrar_login()),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            border=ft.border.only(bottom=ft.BorderSide(1, AZUL)),
        )

    # ==========================
    # LOGIN / REGISTRO
    # ==========================
    # Controles y validaciones de inicio de sesión y creación de cuenta.
    login_empresa = ft.TextField(label="Nombre de la empresa", width=360)
    login_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=360)

    signup_empresa = ft.TextField(label="Nombre de la empresa", width=360)
    signup_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=360)
    signup_pass2 = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=360)

    # Limpia mensajes de error en inputs del login.
    def clear_login_errors():
        login_empresa.error_text = None
        login_pass.error_text = None

    # Limpia mensajes de error en inputs del registro.
    def clear_signup_errors():
        signup_empresa.error_text = None
        signup_pass.error_text = None
        signup_pass2.error_text = None

    # Limpia errores cuando el usuario escriba
    login_empresa.on_change = lambda e: (clear_login_errors(), page.update())
    login_pass.on_change = lambda e: (clear_login_errors(), page.update())

    signup_empresa.on_change = lambda e: (clear_signup_errors(), page.update())
    signup_pass.on_change = lambda e: (clear_signup_errors(), page.update())
    signup_pass2.on_change = lambda e: (clear_signup_errors(), page.update())

    # Maneja el flujo de login con mensajes de error por campo.
    def do_login(e):
        clear_login_errors()

        nombre = (login_empresa.value or "").strip()
        pwd = login_pass.value or ""

        if not nombre:
            login_empresa.error_text = "Ingrese el nombre de la empresa."
            page.update()
            return
        if not pwd:
            login_pass.error_text = "Ingrese la contraseña."
            page.update()
            return

        ok, emp_id, msg = bf.validar_login(nombre, pwd)

        if not ok:
            m = (msg or "").lower()
            if "no encontrada" in m or "empresa" in m and "no" in m:
                login_empresa.error_text = msg
            elif "contraseña" in m:
                login_pass.error_text = msg
            else:
                # fallback
                set_snack(msg, error=True)
            page.update()
            return

        # Login OK
        state["empresa_id"] = emp_id
        state["empresa_nombre"] = nombre
        state["admin_unlocked"] = False
        login_pass.value = ""
        clear_login_errors()
        mostrar_app_principal()

    # Maneja el flujo de registro con validaciones (nombre, password y confirmación).
    def do_signup(e):
        clear_signup_errors()

        nombre = (signup_empresa.value or "").strip()
        p1 = signup_pass.value or ""
        p2 = signup_pass2.value or ""

        if not nombre:
            signup_empresa.error_text = "Ingrese el nombre de la empresa."
            page.update()
            return

        if len(p1) < 4:
            signup_pass.error_text = "La contraseña debe tener al menos 4 caracteres."
            page.update()
            return

        if p1 != p2:
            signup_pass2.error_text = "Las contraseñas no coinciden."
            page.update()
            return

        ok, res = bf.crear_empresa(nombre, p1)

        # Si ya existe, lo mostramos en el input de empresa
        if not ok:
            m = (res or "").lower()
            if "ya existe" in m or "existe una empresa" in m:
                signup_empresa.error_text = res
            else:
                set_snack(res, error=True)
            page.update()
            return

        set_snack("Cuenta creada. Ahora puedes iniciar sesión.")
        signup_empresa.value = ""
        signup_pass.value = ""
        signup_pass2.value = ""
        clear_signup_errors()
        mostrar_login()

    # Renderiza la pantalla de creación de cuenta.
    def mostrar_signup(e=None):
        page.controls.clear()
        page.add(
            ft.Container(height=20),
            ft.Column(
                [
                    ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN),
                    ft.Text("Crear nueva cuenta", size=22, weight=ft.FontWeight.BOLD, color=AZUL),
                    ft.Container(height=10),
                    signup_empresa,
                    signup_pass,
                    signup_pass2,
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.ElevatedButton("Crear cuenta", bgcolor=AZUL, color="white", on_click=do_signup),
                            ft.TextButton("Volver", on_click=mostrar_login),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                spacing=10,
            ),
        )
        page.update()

    # Renderiza la pantalla de login y resetea el estado de sesión.
    def mostrar_login(e=None):
        state["empresa_id"] = None
        state["empresa_nombre"] = None
        state["admin_unlocked"] = False

        page.controls.clear()
        page.add(
            ft.Container(height=20),
            ft.Column(
                [
                    ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN),
                    ft.Text("MicroFinRisk", size=24, weight=ft.FontWeight.BOLD, color=AZUL),
                    ft.Text("Inicio de sesión", size=14, color="black"),
                    ft.Container(height=10),
                    login_empresa,
                    login_pass,
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.ElevatedButton("Iniciar sesión", bgcolor=AZUL, color="white", on_click=do_login),
                            ft.OutlinedButton("Crear nueva cuenta", on_click=mostrar_signup),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                spacing=10,
            ),
        )
        page.update()

    # ==========================
    # TAB: REGISTRO
    # ==========================
    # Formulario para guardar/editar el registro de los primeros 15 días del mes.
    year_dd = ft.Dropdown(
        label="Año",
        width=200,
        options=[ft.dropdown.Option(str(y), text=str(y)) for y in ANIOS],
        value=str(ANIOS[-1]),
    )
    month_dd = ft.Dropdown(
        label="Mes",
        width=200,
        options=[ft.dropdown.Option(str(m), text=nm) for m, nm in MESES],
        value=str(12),
    )
    rubro_field = ft.TextField(label="Rubro (opcional)", width=420, value="General")

    # Crea un TextField numérico compatible con distintas versiones de Flet.
    def num_field(lbl, width=220):
        try:
            return ft.TextField(label=lbl, width=width, input_filter=ft.NumbersOnlyInputFilter())
        except Exception:
            return ft.TextField(label=lbl, width=width, keyboard_type=ft.KeyboardType.NUMBER)

    ventas_15 = num_field("Ventas facturadas (15 días)", 220)   # FACTURADO
    ingresos_15 = num_field("Ingresos cobrados (15 días)", 220) # COBRADO
    gf_15 = num_field("Gastos fijos (15 días)", 220)
    gv_15 = num_field("Gastos variables (15 días)", 220)
    act_15 = num_field("Activos corrientes (15 días)", 220)
    pas_15 = num_field("Pasivos corrientes (15 días)", 220)

    # Textos para mostrar métricas derivadas en tiempo real.
    deriv_gt = ft.Text("Gastos totales (15 días): -", size=12)
    deriv_margen = ft.Text("Margen (15 días): -", size=12)
    deriv_liq = ft.Text("Liquidez (15 días): -", size=12)
    deriv_cobro = ft.Text("Tasa de cobro (15 días): -", size=12)
    deriv_r15 = ft.Text("Riesgo (15 días): -", size=12)

    # Botones del flujo guardar/editar.
    btn_guardar = ft.ElevatedButton("Guardar", bgcolor=AZUL, color="white")
    btn_editar = ft.OutlinedButton("Editar")
    btn_guardar_cambios = ft.ElevatedButton("Guardar cambios", bgcolor=AZUL, color="white")

    # Contenedor donde se renderiza la tabla anual de registros.
    tabla_container = ft.Container()

    # Habilita/deshabilita el formulario (según modo edición).
    def set_form_enabled(enabled: bool):
        for f in [rubro_field, ventas_15, ingresos_15, gf_15, gv_15, act_15, pas_15]:
            f.disabled = not enabled

    # Recalcula y muestra métricas derivadas usando el helper del backend.
    def refresh_derivadas():
        payload = {
            "ventas_15": ventas_15.value,
            "ingresos_15": ingresos_15.value,
            "gastos_fijos_15": gf_15.value,
            "gastos_variables_15": gv_15.value,
            "activos_corrientes_15": act_15.value,
            "pasivos_corrientes_15": pas_15.value,
        }
        tmp = bf._calc_derivadas_15(payload)
        deriv_gt.value = f"Gastos totales (15 días): {fmt_money(tmp.get('gastos_totales_15'))}"
        deriv_margen.value = f"Margen (15 días): {fmt_num(tmp.get('margen_ganancia_15'), 3)}"
        deriv_liq.value = f"Liquidez (15 días): {fmt_num(tmp.get('liquidez_corriente_15'), 3)}"
        deriv_cobro.value = f"Tasa de cobro (15 días): {fmt_pct(tmp.get('tasa_cobro_15'))}"
        deriv_r15.value = f"Riesgo (15 días): {tmp.get('riesgo_15')}"

    # Limpia el formulario para registrar un nuevo mes.
    def clear_form():
        for f in [ventas_15, ingresos_15, gf_15, gv_15, act_15, pas_15]:
            f.value = ""
        rubro_field.value = "General"
        refresh_derivadas()

    # Carga un registro existente del backend dentro del formulario.
    def load_form(rec: dict):
        rubro_field.value = str(rec.get("rubro", "General") or "General")

        def setv(field, val):
            field.value = "" if pd.isna(val) else str(val)

        setv(ventas_15, rec.get("ventas_15"))
        setv(ingresos_15, rec.get("ingresos_15"))
        setv(gf_15, rec.get("gastos_fijos_15"))
        setv(gv_15, rec.get("gastos_variables_15"))
        setv(act_15, rec.get("activos_corrientes_15"))
        setv(pas_15, rec.get("pasivos_corrientes_15"))

        refresh_derivadas()

    # Construye una tabla (DataTable) con todos los meses del año seleccionado.
    def build_tabla_anio(empresa_id: str, anio: int):
        df = bf.obtener_tabla_anio(empresa_id, anio)
        if df is None or len(df) == 0:
            tabla_container.content = ft.Text("No hay registros para este año.", size=12, color="grey")
            return

        # Handler que permite cargar un mes desde la tabla al formulario.
        def on_cargar_mes(mes_val: int):
            def handler(e):
                month_dd.value = str(mes_val)
                on_change_year_month(None)
            return handler

        rows = []
        df["mes"] = pd.to_numeric(df["mes"], errors="coerce").fillna(0).astype(int)
        df = df.sort_values("mes")

        for _, r in df.iterrows():
            mesv = int(r["mes"])
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(mes_nombre(mesv))),
                        ft.DataCell(ft.Text(fmt_money(r.get("ventas_15")))),
                        ft.DataCell(ft.Text(fmt_money(r.get("ingresos_15")))),
                        ft.DataCell(ft.Text(fmt_money(r.get("gastos_totales_15")))),
                        ft.DataCell(ft.Text(fmt_pct(r.get("tasa_cobro_15")))),
                        ft.DataCell(ft.Text(fmt_num(r.get("margen_ganancia_15"), 3))),
                        ft.DataCell(ft.Text(fmt_num(r.get("liquidez_corriente_15"), 3))),
                        ft.DataCell(ft.TextButton("Cargar", on_click=on_cargar_mes(mesv))),
                    ]
                )
            )

        tabla_container.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Mes")),
                ft.DataColumn(ft.Text("Ventas 15d")),
                ft.DataColumn(ft.Text("Ingresos 15d")),
                ft.DataColumn(ft.Text("Gastos 15d")),
                ft.DataColumn(ft.Text("Tasa cobro")),
                ft.DataColumn(ft.Text("Margen")),
                ft.DataColumn(ft.Text("Liquidez")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=rows,
            heading_row_color=ft.Colors.BLUE_50,
            vertical_lines=ft.BorderSide(0.2, ft.Colors.GREY_300),
        )

    # Sincroniza tabla y el formulario cada vez que cambia año/mes.
    def on_change_year_month(e):
        if not state["empresa_id"]:
            return
        anio = int(year_dd.value)
        mes = int(month_dd.value)

        build_tabla_anio(state["empresa_id"], anio)

        rec = bf.obtener_registro_15d(state["empresa_id"], anio, mes)
        if rec:
            load_form(rec)
            set_form_enabled(False)
            btn_guardar.visible = False
            btn_editar.visible = True
            btn_guardar_cambios.visible = False
        else:
            clear_form()
            set_form_enabled(True)
            btn_guardar.visible = True
            btn_editar.visible = False
            btn_guardar_cambios.visible = False

        page.update()

    year_dd.on_change = on_change_year_month
    month_dd.on_change = on_change_year_month

    # Guarda el registro del mes actual en el backend (crea o actualiza).
    def on_click_guardar(e):
        if not state["empresa_id"]:
            return
        anio = int(year_dd.value)
        mes = int(month_dd.value)

        payload = {
            "ventas_15": ventas_15.value,
            "ingresos_15": ingresos_15.value,
            "gastos_fijos_15": gf_15.value,
            "gastos_variables_15": gv_15.value,
            "activos_corrientes_15": act_15.value,
            "pasivos_corrientes_15": pas_15.value,
        }

        ok, msg = bf.upsert_registro_15d(state["empresa_id"], anio, mes, rubro_field.value, payload)
        set_snack(msg, error=not ok)
        on_change_year_month(None)

    # Habilita edición de un registro existente.
    def on_click_editar(e):
        set_form_enabled(True)
        btn_editar.visible = False
        btn_guardar.visible = False
        btn_guardar_cambios.visible = True
        page.update()

    # Guarda cambios y vuelve a modo solo lectura.
    def on_click_guardar_cambios(e):
        on_click_guardar(e)
        set_form_enabled(False)
        btn_editar.visible = True
        btn_guardar.visible = False
        btn_guardar_cambios.visible = False
        page.update()

    btn_guardar.on_click = on_click_guardar
    btn_editar.on_click = on_click_editar
    btn_guardar_cambios.on_click = on_click_guardar_cambios

    # Recalcula derivados cuando cambia cualquier campo numérico.
    for f in [ventas_15, ingresos_15, gf_15, gv_15, act_15, pas_15]:
        f.on_change = lambda e: refresh_derivadas()

    tab_registro = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Text("Registro (primeros 15 días)", size=20, weight=ft.FontWeight.BOLD, color=AZUL),
                ft.Divider(),
                ft.Row([year_dd, month_dd, rubro_field], spacing=12, wrap=True),
                ft.ResponsiveRow(
                    [
                        ft.Container(ventas_15, col={"xs": 12, "md": 4}),
                        ft.Container(ingresos_15, col={"xs": 12, "md": 4}),
                        ft.Container(gf_15, col={"xs": 12, "md": 4}),
                        ft.Container(gv_15, col={"xs": 12, "md": 4}),
                        ft.Container(act_15, col={"xs": 12, "md": 4}),
                        ft.Container(pas_15, col={"xs": 12, "md": 4}),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),
                ft.Row(
                    [
                        ft.Column([deriv_gt, deriv_margen, deriv_liq, deriv_cobro, deriv_r15], spacing=2),
                        ft.Container(expand=True),
                        ft.Row([btn_guardar, btn_editar, btn_guardar_cambios], spacing=10),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Registros del año seleccionado", size=14, weight=ft.FontWeight.BOLD, color=AZUL),
                tabla_container,
            ],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ==========================
    # TAB: PREDICCIONES
    # ==========================
    # UI para seleccionar periodo, ejecutar predicción y mostrar gráficas/recomendaciones.
    pred_year = ft.Dropdown(label="Año", width=200, options=[], on_change=lambda e: refresh_pred_months())
    pred_month = ft.Dropdown(label="Mes", width=200, options=[], on_change=lambda e: refresh_pred_view())
    pred_status = ft.Text("", size=11, color="grey")

    pred_cards_row = ft.Row(spacing=12, wrap=True)

    chart_fin_container = ft.Container()
    chart_prob_container = ft.Container()
    chart_line_container = ft.Container()
    warning_container = ft.Container()
    reco_container = ft.Container()

    # Llena dropdown de años disponibles para predicción.
    def refresh_pred_years():
        if not state["empresa_id"]:
            pred_year.options = []
            pred_month.options = []
            return
        years = bf.listar_anios_con_registros(state["empresa_id"])
        pred_year.options = [ft.dropdown.Option(str(y), text=str(y)) for y in years]
        pred_year.value = str(years[-1]) if years else None
        refresh_pred_months()

    # Llena dropdown de meses según el año elegido.
    def refresh_pred_months():
        if not state["empresa_id"] or not pred_year.value:
            pred_month.options = []
            pred_month.value = None
            refresh_pred_view()
            return
        anio = int(pred_year.value)
        months = bf.listar_meses_con_registros(state["empresa_id"], anio)
        pred_month.options = [ft.dropdown.Option(str(m), text=mes_nombre(m)) for m in months]
        pred_month.value = str(months[-1]) if months else None
        refresh_pred_view()

    # Renderiza la vista completa de predicción (cards, charts, textos).
    def refresh_pred_view():
        pred_cards_row.controls.clear()
        chart_fin_container.content = ft.Container()
        chart_prob_container.content = ft.Container()
        chart_line_container.content = ft.Container()
        warning_container.content = ft.Container()
        reco_container.content = ft.Container()

        if not state["empresa_id"] or not pred_year.value or not pred_month.value:
            pred_status.value = "Seleccione un año y un mes con registros."
            page.update()
            return

        anio = int(pred_year.value)
        mes = int(pred_month.value)

        reg = bf.obtener_registro_15d(state["empresa_id"], anio, mes)
        if not reg:
            pred_status.value = "No existe registro para el periodo seleccionado."
            page.update()
            return

        ok, res, msg = bf.predecir_riesgo_fin_mes(state["empresa_id"], anio, mes)
        if not ok:
            pred_status.value = msg
            chart_fin_container.content = MatplotlibChart(fig_barras_finanzas_15(reg), expand=True)
            page.update()
            return

        riesgo = res.get("riesgo_predicho", "-")
        probs = res.get("probabilidades", {}) or {}

        pred_status.value = f"Modelo: {os.path.basename(res.get('model_path',''))}"

        pred_cards_row.controls.append(make_card("Riesgo estimado fin de mes", str(riesgo), f"{anio}-{mes:02d}"))
        pred_cards_row.controls.append(make_card("Ventas facturadas 15d", fmt_money(reg.get("ventas_15"))))
        pred_cards_row.controls.append(make_card("Ingresos cobrados 15d", fmt_money(reg.get("ingresos_15"))))
        pred_cards_row.controls.append(make_card("Tasa de cobro 15d", fmt_pct(reg.get("tasa_cobro_15")), "Ingresos / Ventas"))
        pred_cards_row.controls.append(make_card("Gastos totales 15d", fmt_money(reg.get("gastos_totales_15"))))

        chart_fin_container.content = MatplotlibChart(fig_barras_finanzas_15(reg), expand=True)
        chart_prob_container.content = MatplotlibChart(fig_probabilidades(probs), expand=True)
        chart_line_container.content = MatplotlibChart(fig_proyeccion_ganancia(reg, str(riesgo)), expand=True)

        warning_container.content = ft.Card(
            content=ft.Container(
                padding=14,
                content=ft.Column(
                    [
                        ft.Text("Advertencia", size=16, weight=ft.FontWeight.BOLD, color=AZUL),
                        ft.Text(generar_advertencia(reg, str(riesgo)), size=12),
                        ft.Text("Nota: la proyección es una simulación basada en la tendencia de 15 días (no es la salida directa del modelo).",
                                size=11, color="grey"),
                    ],
                    spacing=8,
                ),
            )
        )

        recs = generar_recomendaciones(reg, str(riesgo))
        reco_container.content = ft.Card(
            content=ft.Container(
                padding=14,
                content=ft.Column(
                    [
                        ft.Text("Recomendaciones", size=16, weight=ft.FontWeight.BOLD, color=AZUL),
                        ft.Column([ft.Text(f"- {r}", size=12) for r in recs], spacing=6),
                    ],
                    spacing=8,
                ),
            )
        )

        page.update()

    tab_predicciones = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Text("Predicciones", size=20, weight=ft.FontWeight.BOLD, color=AZUL),
                ft.Text("Se muestran riesgo estimado, probabilidades, proyección simulada y recomendaciones.", size=12),
                ft.Divider(),
                ft.Row([pred_year, pred_month], spacing=12, wrap=True),
                pred_status,
                pred_cards_row,
                ft.Divider(),
                ft.ResponsiveRow(
                    [
                        ft.Container(ft.Card(ft.Container(padding=10, content=chart_fin_container)), col={"xs": 12, "md": 6}),
                        ft.Container(ft.Card(ft.Container(padding=10, content=chart_prob_container)), col={"xs": 12, "md": 6}),
                        ft.Container(ft.Card(ft.Container(padding=10, content=chart_line_container)), col={"xs": 12, "md": 12}),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),
                warning_container,
                reco_container,
            ],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ==========================
    # TAB ADMIN
    # ==========================
    # Panel protegido para eliminar registros/meses/años/empresas.
    admin_pwd = ft.TextField(label="Contraseña administrador", password=True, can_reveal_password=True, width=280)
    admin_status = ft.Text("", size=11, color="grey")

    admin_empresa_dd = ft.Dropdown(label="Empresa", width=360, options=[], on_change=lambda e: refresh_admin_years())
    admin_year_dd = ft.Dropdown(label="Año", width=200, options=[], on_change=lambda e: refresh_admin_months())
    admin_month_dd = ft.Dropdown(label="Mes", width=200, options=[])

    btn_del_mes = ft.ElevatedButton("Eliminar mes", bgcolor=ft.Colors.RED_400, color="white")
    btn_del_anio = ft.ElevatedButton("Eliminar año", bgcolor=ft.Colors.RED_400, color="white")
    btn_del_empresa = ft.ElevatedButton("Eliminar empresa", bgcolor=ft.Colors.RED_400, color="white")

    admin_controls = ft.Column(visible=False)

    # Valida la contraseña admin y habilita controles si es correcta.
    def admin_unlock(e):
        if bf.validar_password_admin(admin_pwd.value or ""):
            state["admin_unlocked"] = True
            admin_status.value = "Modo administrador activado."
            refresh_admin_empresas()
        else:
            state["admin_unlocked"] = False
            admin_status.value = "Contraseña incorrecta."
            admin_controls.visible = False
        page.update()

    # Carga empresas disponibles en el dropdown de admin.
    def refresh_admin_empresas():
        if not state["admin_unlocked"]:
            admin_empresa_dd.options = []
            admin_year_dd.options = []
            admin_month_dd.options = []
            admin_controls.visible = False
            return
        df_emp = bf.listar_empresas()
        opts = [ft.dropdown.Option(str(r["empresa_id"]), text=str(r["nombre_empresa"])) for _, r in df_emp.iterrows()]
        admin_empresa_dd.options = opts
        admin_empresa_dd.value = opts[0].key if opts else None
        admin_controls.visible = True
        refresh_admin_years()

    # Carga años disponibles para la empresa seleccionada.
    def refresh_admin_years():
        if not state["admin_unlocked"] or not admin_empresa_dd.value:
            admin_year_dd.options = []
            admin_month_dd.options = []
            return
        years = bf.listar_anios_con_registros(admin_empresa_dd.value)
        admin_year_dd.options = [ft.dropdown.Option(str(y), text=str(y)) for y in years]
        admin_year_dd.value = str(years[-1]) if years else None
        refresh_admin_months()

    # Carga meses disponibles para el año seleccionado.
    def refresh_admin_months():
        if not state["admin_unlocked"] or not admin_empresa_dd.value or not admin_year_dd.value:
            admin_month_dd.options = []
            admin_month_dd.value = None
            return
        months = bf.listar_meses_con_registros(admin_empresa_dd.value, int(admin_year_dd.value))
        admin_month_dd.options = [ft.dropdown.Option(str(m), text=mes_nombre(m)) for m in months]
        admin_month_dd.value = str(months[-1]) if months else None
        page.update()

    # Elimina un mes específico para la empresa/año/mes seleccionado.
    def on_del_mes(e):
        if not state["admin_unlocked"]:
            return
        if not admin_empresa_dd.value or not admin_year_dd.value or not admin_month_dd.value:
            set_snack("Seleccione empresa, año y mes.", error=True)
            return
        ok, msg = bf.eliminar_registro(admin_empresa_dd.value, int(admin_year_dd.value), int(admin_month_dd.value))
        set_snack(msg, error=not ok)
        refresh_admin_years()

    # Elimina todos los meses de un año para la empresa seleccionada.
    def on_del_anio(e):
        if not state["admin_unlocked"]:
            return
        if not admin_empresa_dd.value or not admin_year_dd.value:
            set_snack("Seleccione empresa y año.", error=True)
            return
        ok, msg = bf.eliminar_anio(admin_empresa_dd.value, int(admin_year_dd.value))
        set_snack(msg, error=not ok)
        refresh_admin_years()

    # Elimina empresa y sus datos asociados.
    def on_del_empresa(e):
        if not state["admin_unlocked"]:
            return
        if not admin_empresa_dd.value:
            set_snack("Seleccione empresa.", error=True)
            return
        ok, msg = bf.eliminar_empresa(admin_empresa_dd.value)
        set_snack(msg, error=not ok)
        refresh_admin_empresas()

    btn_del_mes.on_click = on_del_mes
    btn_del_anio.on_click = on_del_anio
    btn_del_empresa.on_click = on_del_empresa

    admin_controls.controls = [
        ft.Divider(),
        ft.Text("Gestión de datos", size=16, weight=ft.FontWeight.BOLD, color=AZUL),
        ft.Row([admin_empresa_dd], spacing=12, wrap=True),
        ft.Row([admin_year_dd, admin_month_dd], spacing=12, wrap=True),
        ft.Row([btn_del_mes, btn_del_anio, btn_del_empresa], spacing=10, wrap=True),
        ft.Text("Los datos se guardan únicamente en data/*.csv.", size=11, color="grey"),
    ]

    tab_admin = ft.Container(
        padding=20,
        content=ft.Column(
            [
                ft.Text("Administración", size=20, weight=ft.FontWeight.BOLD, color=AZUL),
                ft.Text("Acceso protegido para eliminar registros, años o empresas.", size=12),
                ft.Divider(),
                ft.Row(
                    [
                        ft.Text("Acceso administrador:", size=12),
                        admin_pwd,
                        ft.ElevatedButton("Validar", bgcolor=AZUL, color="white", on_click=admin_unlock),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                admin_status,
                admin_controls,
            ],
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # Tabs principales de la aplicación.
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(text="Registro", icon=ft.Icons.EDIT_NOTE, content=tab_registro),
            ft.Tab(text="Predicciones", icon=ft.Icons.QUERY_STATS, content=tab_predicciones),
            ft.Tab(text="Administración", icon=ft.Icons.ADMIN_PANEL_SETTINGS, content=tab_admin),
        ],
        expand=True,
    )
    
    # Renderiza la app luego de iniciar sesión y refresca datos.
    def mostrar_app_principal():
        page.controls.clear()
        page.add(build_header(), tabs)
        on_change_year_month(None)
        refresh_pred_years()
        refresh_admin_empresas()
        page.update()

    # Pantalla inicial.
    mostrar_login()


# Punto de entrada de la app Flet.
if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.abspath(__file__))      # CodeScore/Codigo
    PROJECT_DIR = os.path.dirname(RAIZ)                    # CodeScore
    ASSETS_DIR = os.path.join(PROJECT_DIR, "Recursos")     # CodeScore/Recursos

    ft.app(target=main, assets_dir=ASSETS_DIR)