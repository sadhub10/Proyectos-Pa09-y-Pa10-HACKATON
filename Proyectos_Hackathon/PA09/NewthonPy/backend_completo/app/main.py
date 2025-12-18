"""
FastAPI Application - Sistema de Análisis Inteligente de CSVs
API REST para carga, análisis y clasificación de archivos
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
from pathlib import Path
import shutil
import uuid
from datetime import datetime

# Importar servicios
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.file_parser import FileParser
from app.services.feature_extractor import CSVFeatureExtractor
from app.models.classifier import CSVClassifier

# Configuración
UPLOAD_DIR = Path("/home/claude/backend/data/uploads")
MODELS_DIR = Path("/home/claude/backend/data/models")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Análisis Inteligente de CSVs",
    description="API para clasificación y análisis automático de archivos CSV/Excel",
    version="1.0.0"
)

# CORS (para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo entrenado
classifier = None
feature_extractor = CSVFeatureExtractor()

def load_classifier():
    """Carga el clasificador entrenado"""
    global classifier
    model_path = MODELS_DIR / "csv_classifier.pth"
    
    if not model_path.exists():
        print(f"⚠️  Modelo no encontrado en {model_path}")
        print("⚠️  Por favor entrena el modelo primero con: python training/train_classifier.py")
        return False
    
    try:
        classifier = CSVClassifier.load(str(model_path))
        print(f"✅ Modelo cargado exitosamente desde {model_path}")
        return True
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return False

# Cargar modelo al iniciar
@app.on_event("startup")
async def startup_event():
    """Evento de inicio"""
    print("\n" + "="*70)
    print("  🚀 Iniciando Sistema de Análisis Inteligente de CSVs")
    print("="*70)
    load_classifier()
    print("="*70 + "\n")


# Modelos Pydantic
class FileUploadResponse(BaseModel):
    """Respuesta al subir archivo"""
    file_id: str
    filename: str
    size_bytes: int
    uploaded_at: str
    message: str


class FileInfo(BaseModel):
    """Información del archivo"""
    file_id: str
    filename: str
    n_rows: int
    n_columns: int
    columns: List[str]
    memory_usage_mb: float
    dtypes: Dict[str, str]
    issues: List[Dict[str, Any]]


class ClassificationResult(BaseModel):
    """Resultado de clasificación"""
    file_id: str
    filename: str
    predicted_category: str
    confidence: float
    all_probabilities: Dict[str, float]
    classification_time: float
    features_extracted: int


class AnalysisRequest(BaseModel):
    """Request de análisis"""
    file_id: str
    include_preview: bool = False
    preview_rows: int = 10


class AnalysisResponse(BaseModel):
    """Respuesta de análisis completo"""
    file_info: FileInfo
    classification: ClassificationResult
    preview: Optional[List[Dict[str, Any]]] = None


# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Análisis Inteligente de CSVs",
        "version": "1.0.0",
        "status": "online",
        "model_loaded": classifier is not None
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": classifier is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo CSV o Excel
    
    - **file**: Archivo a subir (CSV, XLSX, XLS)
    
    Returns:
        FileUploadResponse con ID del archivo
    """
    # Validar extensión
    filename = file.filename
    ext = Path(filename).suffix.lower()
    
    if ext not in FileParser.SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Extensión no soportada: {ext}. "
                   f"Soportadas: {', '.join(FileParser.SUPPORTED_EXTENSIONS)}"
        )
    
    # Generar ID único
    file_id = str(uuid.uuid4())
    
    # Guardar archivo
    file_path = UPLOAD_DIR / f"{file_id}_{filename}"
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Obtener tamaño
        size_bytes = file_path.stat().st_size
        
        return FileUploadResponse(
            file_id=file_id,
            filename=filename,
            size_bytes=size_bytes,
            uploaded_at=datetime.now().isoformat(),
            message="Archivo subido exitosamente"
        )
        
    except Exception as e:
        # Limpiar en caso de error
        if file_path.exists():
            file_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error guardando archivo: {str(e)}"
        )


@app.get("/files/{file_id}/info", response_model=FileInfo)
async def get_file_info(file_id: str):
    """
    Obtiene información del archivo
    
    - **file_id**: ID del archivo subido
    
    Returns:
        FileInfo con metadata del archivo
    """
    # Buscar archivo
    files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
    
    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo con ID {file_id} no encontrado"
        )
    
    file_path = files[0]
    
    try:
        # Parsear archivo
        parser = FileParser()
        parser.parse_file(str(file_path))
        
        return FileInfo(
            file_id=file_id,
            filename=parser.metadata['filename'],
            n_rows=parser.metadata['n_rows'],
            n_columns=parser.metadata['n_columns'],
            columns=parser.metadata['columns'],
            memory_usage_mb=parser.metadata['memory_usage_mb'],
            dtypes=parser.metadata['dtypes'],
            issues=parser.metadata['issues']
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando archivo: {str(e)}"
        )


@app.post("/classify/{file_id}", response_model=ClassificationResult)
async def classify_file(file_id: str):
    """
    Clasifica el dominio del archivo usando IA
    
    - **file_id**: ID del archivo subido
    
    Returns:
        ClassificationResult con categoría predicha y confianza
    """
    # Verificar que el modelo esté cargado
    if classifier is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible. Por favor entrena el modelo primero."
        )
    
    # Buscar archivo
    files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
    
    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo con ID {file_id} no encontrado"
        )
    
    file_path = files[0]
    filename = file_path.name.replace(f"{file_id}_", "")
    
    try:
        import time
        start_time = time.time()
        
        # Parsear archivo
        parser = FileParser()
        df = parser.parse_file(str(file_path))
        
        # Extraer features
        features = feature_extractor.extract_features(df, filename)
        
        # Clasificar
        features_reshaped = features.reshape(1, -1)
        prediction, confidence = classifier.predict_with_confidence(features_reshaped)[0]
        
        # Obtener todas las probabilidades
        probas = classifier.predict_proba(features_reshaped)[0]
        all_probabilities = {
            category: float(prob)
            for category, prob in zip(classifier.CATEGORIES, probas)
        }
        
        classification_time = time.time() - start_time
        
        return ClassificationResult(
            file_id=file_id,
            filename=filename,
            predicted_category=prediction,
            confidence=confidence,
            all_probabilities=all_probabilities,
            classification_time=classification_time,
            features_extracted=len(features)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clasificando archivo: {str(e)}"
        )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_file(request: AnalysisRequest):
    """
    Análisis completo: info + clasificación + preview
    
    - **file_id**: ID del archivo
    - **include_preview**: Incluir preview de datos
    - **preview_rows**: Número de filas del preview
    
    Returns:
        AnalysisResponse con análisis completo
    """
    # Obtener info del archivo
    file_info = await get_file_info(request.file_id)
    
    # Clasificar
    classification = await classify_file(request.file_id)
    
    # Preview (opcional)
    preview = None
    if request.include_preview:
        files = list(UPLOAD_DIR.glob(f"{request.file_id}_*"))
        file_path = files[0]
        
        parser = FileParser()
        parser.parse_file(str(file_path))
        preview_df = parser.get_preview(request.preview_rows)
        preview = preview_df.to_dict(orient='records')
    
    return AnalysisResponse(
        file_info=file_info,
        classification=classification,
        preview=preview
    )


@app.get("/files/{file_id}/preview")
async def get_file_preview(
    file_id: str,
    n_rows: int = 10,
    random: bool = False
):
    """
    Obtiene preview del archivo
    
    - **file_id**: ID del archivo
    - **n_rows**: Número de filas
    - **random**: Si True, muestra aleatoria
    
    Returns:
        JSON con preview de los datos
    """
    files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
    
    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo con ID {file_id} no encontrado"
        )
    
    file_path = files[0]
    
    try:
        parser = FileParser()
        parser.parse_file(str(file_path))
        
        if random:
            preview = parser.get_sample(n_rows, random=True)
        else:
            preview = parser.get_preview(n_rows)
        
        return {
            "file_id": file_id,
            "n_rows": len(preview),
            "data": preview.to_dict(orient='records')
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo preview: {str(e)}"
        )


@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """
    Elimina un archivo
    
    - **file_id**: ID del archivo a eliminar
    
    Returns:
        Mensaje de confirmación
    """
    files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
    
    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo con ID {file_id} no encontrado"
        )
    
    try:
        for file_path in files:
            file_path.unlink()
        
        return {
            "message": "Archivo eliminado exitosamente",
            "file_id": file_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando archivo: {str(e)}"
        )


@app.get("/categories")
async def get_categories():
    """
    Obtiene la lista de categorías disponibles
    
    Returns:
        Lista de categorías que el modelo puede predecir
    """
    if classifier is None:
        return {
            "categories": CSVClassifier.CATEGORIES,
            "model_loaded": False
        }
    
    return {
        "categories": classifier.CATEGORIES,
        "model_loaded": True,
        "num_categories": len(classifier.CATEGORIES)
    }


# ========== MAIN ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🚀 Iniciando servidor FastAPI")
    print("="*70)
    print("\n📝 Documentación interactiva:")
    print("  • Swagger UI: http://localhost:8000/docs")
    print("  • ReDoc: http://localhost:8000/redoc")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
