"""
Test End-to-End del Sistema
Prueba el flujo completo: upload → parsing → extracción → clasificación
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import requests
import json
import time

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.file_parser import FileParser
from app.services.feature_extractor import CSVFeatureExtractor
from app.models.classifier import CSVClassifier


def create_sample_datasets():
    """Crea datasets de ejemplo para cada categoría"""
    
    samples = {}
    
    # 1. Finanzas
    samples['finanzas'] = pd.DataFrame({
        'fecha_transaccion': pd.date_range('2024-01-01', periods=50),
        'monto': np.random.uniform(10, 10000, 50),
        'tipo': np.random.choice(['ingreso', 'gasto'], 50),
        'categoria': np.random.choice(['ventas', 'compras', 'servicios'], 50),
        'cuenta': [f'ACC{i:04d}' for i in range(50)],
        'balance': np.cumsum(np.random.randn(50) * 100)
    })
    
    # 2. Educación
    samples['educacion'] = pd.DataFrame({
        'alumno_id': [f'EST{i:04d}' for i in range(50)],
        'nombre': [f'Estudiante {i}' for i in range(50)],
        'materia': np.random.choice(['Matemáticas', 'Historia', 'Ciencias', 'Inglés'], 50),
        'calificacion': np.random.uniform(0, 100, 50),
        'asistencia': np.random.uniform(70, 100, 50),
        'profesor': np.random.choice(['Prof. García', 'Prof. López', 'Prof. Martínez'], 50)
    })
    
    # 3. Ventas
    samples['ventas'] = pd.DataFrame({
        'orden_id': [f'ORD{i:05d}' for i in range(50)],
        'producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], 50),
        'cantidad': np.random.randint(1, 10, 50),
        'precio_unitario': np.random.uniform(10, 1000, 50),
        'cliente': [f'Cliente {i}' for i in np.random.randint(1, 20, 50)],
        'fecha_venta': pd.date_range('2024-01-01', periods=50),
        'descuento': np.random.uniform(0, 20, 50)
    })
    
    # 4. RRHH
    samples['rrhh'] = pd.DataFrame({
        'empleado_id': [f'EMP{i:04d}' for i in range(50)],
        'nombre': [f'Empleado {i}' for i in range(50)],
        'departamento': np.random.choice(['IT', 'Ventas', 'RRHH', 'Finanzas'], 50),
        'cargo': np.random.choice(['Analista', 'Manager', 'Director'], 50),
        'salario': np.random.uniform(30000, 120000, 50),
        'fecha_ingreso': pd.date_range('2020-01-01', periods=50),
        'beneficios': np.random.uniform(5000, 20000, 50)
    })
    
    return samples


def test_feature_extraction():
    """Prueba 1: Extracción de features"""
    print("\n" + "="*70)
    print("  TEST 1: Extracción de Features")
    print("="*70)
    
    samples = create_sample_datasets()
    extractor = CSVFeatureExtractor()
    
    results = {}
    
    for category, df in samples.items():
        print(f"\nProcesando: {category.upper()}")
        
        # Extraer features
        features = extractor.extract_features(df)
        
        print(f"  ✓ Features extraídas: {len(features)}")
        print(f"  ✓ Shape: {features.shape}")
        print(f"  ✓ Primeras 5 features: {features[:5]}")
        
        results[category] = features
    
    print(f"\nExtracción completada para {len(results)} categorías")
    return results


def test_classification(features_by_category):
    """Prueba 2: Clasificación"""
    print("\n" + "="*70)
    print("  TEST 2: Clasificación con Modelo Entrenado")
    print("="*70)
    
    model_path = '/home/claude/backend/data/models/csv_classifier.pth'
    
    if not Path(model_path).exists():
        print(f"\nModelo no encontrado en {model_path}")
        print("Por favor entrena el modelo primero:")
        print("    cd /home/claude/backend/training")
        print("    python train_classifier.py")
        return False
    
    # Cargar modelo
    print(f"\nCargando modelo desde {model_path}...")
    classifier = CSVClassifier.load(model_path)
    print(f"Modelo cargado")
    print(f"  Device: {classifier.device}")
    print(f"  Categorías: {classifier.CATEGORIES}")
    
    # Clasificar cada muestra
    print(f"\nClasificando muestras...")
    
    for true_category, features in features_by_category.items():
        features_reshaped = features.reshape(1, -1)
        
        # Predecir
        pred_category, confidence = classifier.predict_with_confidence(features_reshaped)[0]
        
        # Mostrar resultado
        is_correct = "" if pred_category == true_category else ""
        print(f"\n  {is_correct} Real: {true_category:12} | Predicho: {pred_category:12} | Confianza: {confidence:.2%}")
        
        # Mostrar top 3 probabilidades
        probas = classifier.predict_proba(features_reshaped)[0]
        top_3_idx = np.argsort(probas)[-3:][::-1]
        
        print(f"     Top 3 probabilidades:")
        for idx in top_3_idx:
            cat = classifier.CATEGORIES[idx]
            prob = probas[idx]
            print(f"       {cat:12}: {prob:.2%}")
    
    print(f"\nClasificación completada")
    return True


def test_file_parser():
    """Prueba 3: Parser de archivos"""
    print("\n" + "="*70)
    print("  TEST 3: Parser de Archivos")
    print("="*70)
    
    # Crear CSV temporal
    samples = create_sample_datasets()
    test_file = '/tmp/test_ventas.csv'
    samples['ventas'].to_csv(test_file, index=False)
    
    print(f"\nArchivo creado: {test_file}")
    
    # Parsear
    parser = FileParser()
    df = parser.parse_file(test_file)
    
    print(f"\nArchivo parseado exitosamente")
    print(f"  Filas: {len(df)}")
    print(f"  Columnas: {len(df.columns)}")
    print(f"  Tamaño: {parser.metadata['memory_usage_mb']:.2f} MB")
    
    print(f"\nInformación de columnas:")
    for col, info in list(parser.metadata['column_info'].items())[:3]:
        print(f"\n  {col}:")
        print(f"    Tipo: {info['dtype']}")
        print(f"    Nulos: {info['null_count']} ({info['null_percentage']:.1f}%)")
        print(f"    Únicos: {info['unique_count']}")
    
    print(f"\n Issues detectados: {len(parser.metadata['issues'])}")
    for issue in parser.metadata['issues']:
        print(f"  - {issue['message']}")
    
    print(f"\n Preview (primeras 3 filas):")
    print(parser.get_preview(3))
    
    # Limpiar
    import os
    os.remove(test_file)
    
    print(f"\nTest de parser completado")
    return True


def test_end_to_end_workflow():
    """Prueba 4: Flujo completo end-to-end"""
    print("\n" + "="*70)
    print("  TEST 4: Flujo End-to-End Completo")
    print("="*70)
    
    # Verificar modelo
    model_path = '/home/claude/backend/data/models/csv_classifier.pth'
    if not Path(model_path).exists():
        print(f"\nModelo no encontrado. Saltando test end-to-end.")
        return False
    
    # 1. Crear archivo
    print(f"\nPASO 1: Crear archivo de prueba")
    samples = create_sample_datasets()
    test_file = '/tmp/test_finanzas.csv'
    samples['finanzas'].to_csv(test_file, index=False)
    print(f"  ✓ Archivo creado: {test_file}")
    
    # 2. Parsear
    print(f"\nPASO 2: Parsear archivo")
    parser = FileParser()
    df = parser.parse_file(test_file)
    print(f"  ✓ Parseado: {len(df)} filas, {len(df.columns)} columnas")
    
    # 3. Extraer features
    print(f"\n🔬 PASO 3: Extraer features")
    extractor = CSVFeatureExtractor()
    features = extractor.extract_features(df)
    print(f"  ✓ Features extraídas: {len(features)}")
    
    # 4. Clasificar
    print(f"\n🎯 PASO 4: Clasificar")
    classifier = CSVClassifier.load(model_path)
    features_reshaped = features.reshape(1, -1)
    pred_category, confidence = classifier.predict_with_confidence(features_reshaped)[0]
    print(f"  ✓ Categoría predicha: {pred_category}")
    print(f"  ✓ Confianza: {confidence:.2%}")
    
    # 5. Resultado
    print(f"\nRESULTADO FINAL:")
    print(f"  Archivo: test_finanzas.csv")
    print(f"  Categoría real: finanzas")
    print(f"  Categoría predicha: {pred_category}")
    print(f"  Confianza: {confidence:.2%}")
    print(f"  ¿Correcto?: {' SÍ' if pred_category == 'finanzas' else 'NO'}")
    
    # Limpiar
    import os
    os.remove(test_file)
    
    print(f"\nFlujo end-to-end completado")
    return True


def test_api_endpoints():
    """Prueba 5: Endpoints de la API (requiere servidor corriendo)"""
    print("\n" + "="*70)
    print("  TEST 5: Endpoints de la API")
    print("="*70)
    
    base_url = "http://localhost:8000"
    
    # Verificar si el servidor está corriendo
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        if response.status_code != 200:
            print(f"\n Servidor no responde. Por favor inicia el servidor:")
            print(f"    cd /home/claude/backend/app")
            print(f"    python main.py")
            return False
    except requests.exceptions.RequestException:
        print(f"\n No se puede conectar al servidor en {base_url}")
        print(f"    Por favor inicia el servidor primero:")
        print(f"    cd /home/claude/backend/app")
        print(f"    python main.py")
        return False
    
    print(f"\n Servidor detectado en {base_url}")
    
    # 1. Health check
    print(f"\n Test 1: Health Check")
    response = requests.get(f"{base_url}/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    # 2. Categorías disponibles
    print(f"\n Test 2: Categorías Disponibles")
    response = requests.get(f"{base_url}/categories")
    data = response.json()
    print(f"  Categorías: {data['categories']}")
    print(f"  Modelo cargado: {data['model_loaded']}")
    
    # 3. Upload archivo
    print(f"\n Test 3: Upload Archivo")
    samples = create_sample_datasets()
    test_file = '/tmp/api_test.csv'
    samples['ventas'].to_csv(test_file, index=False)
    
    with open(test_file, 'rb') as f:
        files = {'file': ('test_ventas.csv', f, 'text/csv')}
        response = requests.post(f"{base_url}/upload", files=files)
    
    upload_result = response.json()
    file_id = upload_result['file_id']
    print(f"  File ID: {file_id}")
    print(f"  Filename: {upload_result['filename']}")
    print(f"  Size: {upload_result['size_bytes']} bytes")
    
    # 4. Análisis completo
    print(f"\n Test 4: Análisis Completo")
    response = requests.post(
        f"{base_url}/analyze",
        json={
            "file_id": file_id,
            "include_preview": True,
            "preview_rows": 5
        }
    )
    
    analysis = response.json()
    print(f"  Categoría predicha: {analysis['classification']['predicted_category']}")
    print(f"  Confianza: {analysis['classification']['confidence']:.2%}")
    print(f"  Filas: {analysis['file_info']['n_rows']}")
    print(f"  Columnas: {analysis['file_info']['n_columns']}")
    
    # 5. Limpiar
    print(f"\n  Test 5: Eliminar Archivo")
    response = requests.delete(f"{base_url}/files/{file_id}")
    print(f"  Status: {response.status_code}")
    print(f"  Message: {response.json()['message']}")
    
    # Limpiar archivo local
    import os
    os.remove(test_file)
    
    print(f"\n Tests de API completados")
    return True


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print("   SUITE DE TESTS - Sistema de Análisis de CSVs")
    print("="*70)
    
    results = {}
    
    # Test 1: Feature Extraction
    try:
        features = test_feature_extraction()
        results['feature_extraction'] = True
    except Exception as e:
        print(f"\n Error en test 1: {e}")
        results['feature_extraction'] = False
        features = None
    
    # Test 2: Classification
    if features:
        try:
            results['classification'] = test_classification(features)
        except Exception as e:
            print(f"\n Error en test 2: {e}")
            results['classification'] = False
    else:
        results['classification'] = False
    
    # Test 3: File Parser
    try:
        results['file_parser'] = test_file_parser()
    except Exception as e:
        print(f"\n Error en test 3: {e}")
        results['file_parser'] = False
    
    # Test 4: End-to-End
    try:
        results['end_to_end'] = test_end_to_end_workflow()
    except Exception as e:
        print(f"\n Error en test 4: {e}")
        results['end_to_end'] = False
    
    # Test 5: API (opcional, requiere servidor)
    try:
        results['api'] = test_api_endpoints()
    except Exception as e:
        print(f"\nError en test 5: {e}")
        results['api'] = False
    
    # Resume
    print("\n" + "="*70)
    print("  📊 RESUMEN DE TESTS")
    print("="*70)
    
    for test_name, passed in results.items():
        status = " PASSED" if passed else " FAILED"
        print(f"  {test_name:20}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n  Total: {passed}/{total} tests pasados ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n   ¡Todos los tests pasaron exitosamente!")
    else:
        print(f"\n    {total - passed} test(s) fallaron")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
