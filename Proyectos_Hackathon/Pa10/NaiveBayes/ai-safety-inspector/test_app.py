"""
Script de prueba para verificar el funcionamiento de la aplicación
"""

import os
import sys
from PIL import Image
import numpy as np

def test_model_loading():
    """Prueba que el modelo se cargue correctamente"""
    print("🧪 Probando carga del modelo...")
    try:
        from ultralytics import YOLO
        
        if os.path.exists('best.pt'):
            model = YOLO('best.pt')
            print("✅ Modelo personalizado cargado")
        else:
            model = YOLO('yolov8n.pt')
            print("✅ Modelo YOLOv8n cargado")
        
        return True, model
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        return False, None

def create_test_image():
    """Crea una imagen de prueba simple"""
    print("\n🎨 Creando imagen de prueba...")
    
    # Crear imagen de prueba (simulación)
    img = Image.new('RGB', (640, 480), color='white')
    
    # Guardar
    if not os.path.exists('images'):
        os.makedirs('images')
    
    test_path = 'images/test_image.jpg'
    img.save(test_path)
    print(f"✅ Imagen de prueba guardada en: {test_path}")
    return test_path

def test_detection(model, image_path):
    """Prueba la detección en una imagen"""
    print("\n🔍 Probando detección...")
    try:
        # Cargar imagen
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Ejecutar detección
        results = model(img_array, conf=0.3)
        
        # Contar detecciones
        total_detections = 0
        for result in results:
            total_detections += len(result.boxes)
        
        print(f"✅ Detección exitosa: {total_detections} objetos detectados")
        return True
    except Exception as e:
        print(f"❌ Error en detección: {e}")
        return False

def test_streamlit_import():
    """Verifica que Streamlit se pueda importar"""
    print("\n🌊 Probando Streamlit...")
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar Streamlit: {e}")
        return False

def test_opencv():
    """Verifica OpenCV"""
    print("\n📷 Probando OpenCV...")
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} funcionando")
        return True
    except Exception as e:
        print(f"❌ Error con OpenCV: {e}")
        return False

def test_plotly():
    """Verifica Plotly"""
    print("\n📊 Probando Plotly...")
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Crear un gráfico simple de prueba
        fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])
        print("✅ Plotly funcionando correctamente")
        return True
    except Exception as e:
        print(f"❌ Error con Plotly: {e}")
        return False

def check_file_structure():
    """Verifica que todos los archivos necesarios existan"""
    print("\n📂 Verificando estructura de archivos...")
    
    required_files = {
        'app.py': 'Aplicación principal',
        'requirements.txt': 'Dependencias',
        'README.md': 'Documentación'
    }
    
    all_present = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - FALTANTE")
            all_present = False
    
    return all_present

def print_system_info():
    """Imprime información del sistema"""
    print("\n💻 INFORMACIÓN DEL SISTEMA")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"Sistema Operativo: {os.name}")
    
    try:
        import torch
        print(f"PyTorch: {torch.__version__}")
        print(f"CUDA disponible: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
    except:
        print("PyTorch: No instalado")
    
    print("="*60)

def download_sample_images():
    """Descarga imágenes de ejemplo desde URLs públicas"""
    print("\n🖼️  Descargando imágenes de ejemplo...")
    
    try:
        import urllib.request
        
        sample_urls = [
            ('https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400', 'construction_1.jpg'),
            ('https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=400', 'construction_2.jpg'),
        ]
        
        if not os.path.exists('images'):
            os.makedirs('images')
        
        for url, filename in sample_urls:
            filepath = os.path.join('images', filename)
            if not os.path.exists(filepath):
                try:
                    urllib.request.urlretrieve(url, filepath)
                    print(f"✅ Descargado: {filename}")
                except:
                    print(f"⚠️  No se pudo descargar: {filename}")
            else:
                print(f"ℹ️  Ya existe: {filename}")
    except Exception as e:
        print(f"⚠️  Error al descargar imágenes: {e}")
        print("   Puedes agregar tus propias imágenes en la carpeta 'images/'")

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("="*60)
    print("🧪 PRUEBAS DE LA APLICACIÓN")
    print("="*60)
    
    # Info del sistema
    print_system_info()
    
    # Verificar archivos
    files_ok = check_file_structure()
    
    # Probar librerías
    streamlit_ok = test_streamlit_import()
    opencv_ok = test_opencv()
    plotly_ok = test_plotly()
    
    # Probar modelo
    model_ok, model = test_model_loading()
    
    # Crear imagen de prueba
    if model_ok:
        test_img = create_test_image()
        detection_ok = test_detection(model, test_img)
    else:
        detection_ok = False
    
    # Descargar imágenes de ejemplo
    download_sample_images()
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    tests = {
        'Estructura de archivos': files_ok,
        'Streamlit': streamlit_ok,
        'OpenCV': opencv_ok,
        'Plotly': plotly_ok,
        'Modelo YOLO': model_ok,
        'Detección': detection_ok
    }
    
    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(tests.values())
    
    print("="*60)
    if all_passed:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n✅ La aplicación está lista para usar")
        print("\n🚀 Ejecuta: streamlit run app.py")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("\n📝 Revisa los errores arriba y:")
        print("   1. Verifica que todas las dependencias estén instaladas")
        print("   2. Ejecuta: python setup.py")
        print("   3. Si persisten errores, revisa el README.md")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
