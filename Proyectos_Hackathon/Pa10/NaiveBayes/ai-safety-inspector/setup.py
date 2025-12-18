"""
Script de configuración para AI Safety Inspector
Descarga automáticamente el modelo YOLOv8 y verifica las dependencias
"""

import os
import sys
import subprocess

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def install_requirements():
    """Instala las dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def download_yolo_model():
    """Descarga el modelo YOLOv8 si no existe"""
    print("\n🤖 Verificando modelo YOLOv8...")
    
    # Verificar si ya existe un modelo
    if os.path.exists('best.pt'):
        print("✅ Modelo personalizado 'best.pt' encontrado")
        return True
    
    if os.path.exists('yolov8n.pt'):
        print("✅ Modelo YOLOv8n encontrado")
        return True
    
    print("📥 Descargando modelo YOLOv8n (base)...")
    try:
        from ultralytics import YOLO
        # Esto descargará automáticamente el modelo
        model = YOLO('yolov8n.pt')
        print("✅ Modelo YOLOv8n descargado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al descargar el modelo: {e}")
        return False

def create_directories():
    """Crea directorios necesarios"""
    print("\n📁 Creando estructura de directorios...")
    dirs = ['images', 'reports']
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Directorio '{dir_name}' creado")
        else:
            print(f"ℹ️  Directorio '{dir_name}' ya existe")

def test_imports():
    """Prueba que todas las librerías se puedan importar"""
    print("\n🧪 Probando imports...")
    
    libraries = [
        'streamlit',
        'cv2',
        'numpy',
        'PIL',
        'torch',
        'ultralytics',
        'plotly'
    ]
    
    failed = []
    for lib in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib}")
        except ImportError:
            print(f"❌ {lib}")
            failed.append(lib)
    
    if failed:
        print(f"\n⚠️  Librerías faltantes: {', '.join(failed)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todas las librerías están instaladas correctamente")
    return True

def create_example_config():
    """Crea un archivo de configuración de ejemplo para Streamlit"""
    config_dir = '.streamlit'
    config_file = os.path.join(config_dir, 'config.toml')
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        config_content = """[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"✅ Archivo de configuración creado en {config_file}")

def print_next_steps():
    """Imprime los siguientes pasos para el usuario"""
    print("\n" + "="*60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("="*60)
    print("\n📋 PRÓXIMOS PASOS:\n")
    print("1. Para ejecutar la aplicación:")
    print("   streamlit run app.py\n")
    print("2. La aplicación se abrirá en: http://localhost:8501\n")
    print("3. Para mejor rendimiento, considera:")
    print("   - Descargar un modelo personalizado de Kaggle")
    print("   - Colocar el archivo 'best.pt' en esta carpeta\n")
    print("4. Datasets recomendados:")
    print("   - Hard Hat Detection: https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection")
    print("   - Construction Site Safety: https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow\n")
    print("="*60)
    print("\n🚀 ¡Listo para tu hackathon! ¡Buena suerte!\n")

def main():
    """Función principal"""
    print("="*60)
    print("🦺 AI SAFETY INSPECTOR - CONFIGURACIÓN")
    print("="*60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_requirements():
        print("\n⚠️  Instala las dependencias manualmente:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Probar imports
    if not test_imports():
        sys.exit(1)
    
    # Descargar modelo
    download_yolo_model()
    
    # Crear directorios
    create_directories()
    
    # Crear configuración
    create_example_config()
    
    # Mostrar siguientes pasos
    print_next_steps()

if __name__ == "__main__":
    main()
