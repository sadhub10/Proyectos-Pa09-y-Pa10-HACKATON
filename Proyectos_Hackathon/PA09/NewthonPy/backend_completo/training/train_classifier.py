"""
Script de Entrenamiento del Clasificador de CSVs
Descarga datasets reales de Kaggle y entrena el modelo desde cero

REQUISITOS:
1. Cuenta en Kaggle (gratis)
2. API token de Kaggle en ~/.kaggle/kaggle.json
3. pip install kaggle

Para obtener el token:
1. Ir a https://www.kaggle.com/settings
2. Crear nuevo API token
3. Descargar kaggle.json
4. Mover a ~/.kaggle/kaggle.json
5. chmod 600 ~/.kaggle/kaggle.json
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import json
import shutil
from tqdm import tqdm

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.feature_extractor import CSVFeatureExtractor
from app.models.classifier import CSVClassifier


class DatasetDownloader:
    """Descarga y organiza datasets de Kaggle por categoría"""
    
    # Datasets públicos de Kaggle por categoría
    DATASETS_BY_CATEGORY = {
        'finanzas': [
            'mlg-ulb/creditcardfraud',  # Transacciones bancarias
            'ukveteran/credit-card-transactions',
            'whenamancodes/fraud-detection',
        ],
        'educacion': [
            'mohansacharya/graduate-admissions',
            'aljarah/xAPI-Edu-Data',
            'lperez/student-performance',
        ],
        'ventas': [
            'c0d3xzz/online-retail-dataset',
            'carrie1/ecommerce-data',
            'mkechinov/ecommerce-behavior-data-from-multi-category-store',
        ],
        'rrhh': [
            'rhuebner/human-resources-data-set',
            'vjchoudhary7/hr-analytics-case-study',
            'pavansubhasht/ibm-hr-analytics-attrition-dataset',
        ],
        'inventario': [
            'felixzhao/productdemandforecasting',
            'bhanupratapbiswas/inventory-management-system',
        ],
        'marketing': [
            'loveall/clicks-conversion-tracking',
            'rodsaldanha/arketing-campaign',
        ],
        'salud': [
            'jimschacko/hospitals-in-united-states',
            'uom190346a/disease-symptoms-and-patient-profile-dataset',
        ],
        'logistica': [
            'prachi13/customer-analytics',
            'satyamjay/supply-chain-shipment-pricing-data',
        ],
    }
    
    def __init__(self, data_dir: str = '/home/claude/backend/data'):
        """
        Args:
            data_dir: Directorio base para guardar datos
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        self.models_dir = self.data_dir / 'models'
        
        # Crear directorios
        for dir_path in [self.raw_dir, self.processed_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def download_datasets(self, max_per_category: int = 2, force: bool = False):
        """
        Descarga datasets de Kaggle
        
        Args:
            max_per_category: Máximo de datasets por categoría
            force: Re-descargar aunque ya existan
        """
        print("🔽 Descargando datasets de Kaggle...")
        print("⚠️  Asegúrate de tener configurado tu token de Kaggle\n")
        
        # Verificar configuración de Kaggle
        kaggle_config = Path.home() / '.kaggle' / 'kaggle.json'
        if not kaggle_config.exists():
            print("❌ ERROR: No se encontró ~/.kaggle/kaggle.json")
            print("Por favor configura tu API token de Kaggle:")
            print("1. Ve a https://www.kaggle.com/settings")
            print("2. Crea un nuevo API token")
            print("3. Descarga kaggle.json")
            print("4. Muévelo a ~/.kaggle/kaggle.json")
            print("5. Ejecuta: chmod 600 ~/.kaggle/kaggle.json")
            return False
        
        try:
            import kaggle
        except ImportError:
            print("❌ ERROR: pip install kaggle")
            return False
        
        downloaded = {}
        
        for category, dataset_list in self.DATASETS_BY_CATEGORY.items():
            print(f"\n📂 Categoría: {category.upper()}")
            downloaded[category] = []
            
            for i, dataset_name in enumerate(dataset_list[:max_per_category], 1):
                category_dir = self.raw_dir / category
                category_dir.mkdir(exist_ok=True)
                
                # Directorio destino para este dataset
                dataset_slug = dataset_name.split('/')[-1]
                dest_dir = category_dir / dataset_slug
                
                if dest_dir.exists() and not force:
                    print(f"  ✓ [{i}/{max_per_category}] {dataset_name} (ya existe)")
                    downloaded[category].append(dest_dir)
                    continue
                
                try:
                    print(f"  ⬇️  [{i}/{max_per_category}] Descargando {dataset_name}...")
                    
                    # Descargar
                    kaggle.api.dataset_download_files(
                        dataset_name,
                        path=str(dest_dir),
                        unzip=True,
                        quiet=False
                    )
                    
                    downloaded[category].append(dest_dir)
                    print(f"  ✅ Descargado: {dataset_name}")
                    
                except Exception as e:
                    print(f"  ❌ Error descargando {dataset_name}: {str(e)}")
                    continue
        
        # Guardar índice de datasets descargados
        index_file = self.raw_dir / 'dataset_index.json'
        with open(index_file, 'w') as f:
            json.dump({
                cat: [str(p) for p in paths]
                for cat, paths in downloaded.items()
            }, f, indent=2)
        
        print(f"\n✅ Datasets descargados. Índice guardado en: {index_file}")
        return True
    
    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepara datos de entrenamiento a partir de datasets descargados
        
        Returns:
            (features, labels, filenames)
        """
        print("\n🔧 Preparando datos de entrenamiento...")
        
        extractor = CSVFeatureExtractor()
        feature_list = []
        label_list = []
        filename_list = []
        
        # Mapeo categoría -> índice
        category_to_idx = {
            cat: idx for idx, cat in enumerate(CSVClassifier.CATEGORIES)
        }
        
        # Procesar cada categoría
        for category in tqdm(self.DATASETS_BY_CATEGORY.keys(), desc="Categorías"):
            category_dir = self.raw_dir / category
            
            if not category_dir.exists():
                print(f"⚠️  No se encontró {category_dir}, saltando...")
                continue
            
            # Buscar todos los CSVs en esta categoría
            csv_files = list(category_dir.rglob('*.csv'))
            
            print(f"\n  {category}: {len(csv_files)} archivos CSV encontrados")
            
            for csv_file in csv_files:
                try:
                    # Leer CSV
                    df = pd.read_csv(csv_file, nrows=1000)  # Solo primeras 1000 filas
                    
                    # Validar que tenga datos
                    if len(df) < 10 or len(df.columns) < 2:
                        continue
                    
                    # Extraer features
                    features = extractor.extract_features(df, str(csv_file))
                    
                    # Agregar a listas
                    feature_list.append(features)
                    label_list.append(category_to_idx[category])
                    filename_list.append(str(csv_file.name))
                    
                except Exception as e:
                    print(f"    ⚠️  Error procesando {csv_file.name}: {str(e)}")
                    continue
        
        if not feature_list:
            print("❌ No se pudieron extraer features de ningún archivo")
            return None, None, None
        
        # Convertir a arrays
        X = np.array(feature_list, dtype=np.float32)
        y = np.array(label_list, dtype=np.int64)
        
        print(f"\n✅ Datos preparados:")
        print(f"   Shape de X: {X.shape}")
        print(f"   Shape de y: {y.shape}")
        print(f"   Distribución de clases:")
        
        for cat_name, cat_idx in category_to_idx.items():
            count = (y == cat_idx).sum()
            if count > 0:
                print(f"     {cat_name}: {count} samples")
        
        # Guardar datos procesados
        np.save(self.processed_dir / 'X_train.npy', X)
        np.save(self.processed_dir / 'y_train.npy', y)
        
        with open(self.processed_dir / 'filenames.json', 'w') as f:
            json.dump(filename_list, f, indent=2)
        
        print(f"\n💾 Datos guardados en {self.processed_dir}")
        
        return X, y, filename_list


def train_classifier(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    epochs: int = 150,
    batch_size: int = 32,
    learning_rate: float = 0.001
):
    """
    Entrena el clasificador
    
    Args:
        X: Features
        y: Labels
        test_size: Proporción de datos para validación
        epochs: Número de épocas
        batch_size: Tamaño de batch
        learning_rate: Learning rate
    """
    print("\n🚀 Iniciando entrenamiento del modelo...")
    
    # Split train/validation
    n_samples = len(X)
    indices = np.random.permutation(n_samples)
    split = int(n_samples * (1 - test_size))
    
    train_idx, val_idx = indices[:split], indices[split:]
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    print(f"  Training samples: {len(X_train)}")
    print(f"  Validation samples: {len(X_val)}")
    print(f"  Features: {X.shape[1]}")
    print()
    
    # Crear clasificador
    classifier = CSVClassifier(input_size=X.shape[1])
    print(f"  Device: {classifier.device}")
    print(f"  Categorías: {classifier.CATEGORIES}")
    print()
    
    # Entrenar
    metrics = classifier.train(
        X_train, y_train,
        X_val, y_val,
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        verbose=True
    )
    
    # Evaluación final
    print("\n📊 Evaluación Final")
    eval_metrics = classifier.evaluate(X_val, y_val)
    
    for metric, value in eval_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Guardar modelo
    model_path = '/home/claude/backend/data/models/csv_classifier.pth'
    classifier.save(model_path)
    
    print(f"\n✅ Modelo guardado en: {model_path}")
    
    return classifier, metrics


def main():
    """Función principal de entrenamiento"""
    print("=" * 70)
    print("  ENTRENAMIENTO DE CLASIFICADOR DE CSVs")
    print("=" * 70)
    
    # Configuración
    downloader = DatasetDownloader()
    
    # Paso 1: Descargar datasets
    print("\n📥 PASO 1: Descargar Datasets")
    print("-" * 70)
    
    success = downloader.download_datasets(
        max_per_category=2,  # 2 datasets por categoría (ajustar según necesidad)
        force=False  # No re-descargar si ya existen
    )
    
    if not success:
        print("\n❌ Error en la descarga. Por favor configura Kaggle correctamente.")
        return
    
    # Paso 2: Preparar datos de entrenamiento
    print("\n🔧 PASO 2: Preparar Datos de Entrenamiento")
    print("-" * 70)
    
    X, y, filenames = downloader.prepare_training_data()
    
    if X is None:
        print("\n❌ No se pudieron preparar los datos.")
        return
    
    # Paso 3: Entrenar modelo
    print("\n🎓 PASO 3: Entrenar Modelo")
    print("-" * 70)
    
    classifier, metrics = train_classifier(
        X, y,
        test_size=0.2,
        epochs=150,
        batch_size=32,
        learning_rate=0.001
    )
    
    print("\n" + "=" * 70)
    print("  ✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 70)
    print(f"\nModelo guardado en: /home/claude/backend/data/models/csv_classifier.pth")
    print("Puedes cargar el modelo con: CSVClassifier.load(path)")


if __name__ == "__main__":
    # Verificar dependencias
    try:
        import kaggle
        import torch
        import sklearn
        from tqdm import tqdm
        
        print("✅ Todas las dependencias están instaladas\n")
        main()
        
    except ImportError as e:
        print(f"❌ Falta instalar: {str(e)}")
        print("\nInstala las dependencias con:")
        print("pip install kaggle torch scikit-learn tqdm pandas numpy")
