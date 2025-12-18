"""
Feature Extractor para Clasificación de CSVs
Extrae características numéricas de archivos CSV para entrenar el clasificador
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import re
from collections import Counter
from scipy import stats


class CSVFeatureExtractor:
    """
    Extrae features de CSVs para clasificación automática de dominio
    """
    
    # Keywords por categoría (expandir con más ejemplos)
    DOMAIN_KEYWORDS = {
        'finanzas': [
            'precio', 'cost', 'ingreso', 'revenue', 'gasto', 'expense', 
            'balance', 'profit', 'pérdida', 'loss', 'factura', 'invoice',
            'pago', 'payment', 'cuenta', 'account', 'transaccion', 'transaction',
            'credito', 'debito', 'saldo', 'total', 'monto', 'amount'
        ],
        'educacion': [
            'alumno', 'student', 'profesor', 'teacher', 'calificacion', 'grade',
            'nota', 'score', 'materia', 'subject', 'curso', 'course', 'examen',
            'exam', 'tarea', 'homework', 'asistencia', 'attendance', 'promedio',
            'average', 'semestre', 'periodo', 'escuela', 'colegio', 'universidad'
        ],
        'ventas': [
            'venta', 'sale', 'producto', 'product', 'cliente', 'customer',
            'cantidad', 'quantity', 'precio', 'price', 'descuento', 'discount',
            'total', 'subtotal', 'iva', 'tax', 'orden', 'order', 'pedido',
            'compra', 'factura', 'categoria', 'stock', 'inventario'
        ],
        'rrhh': [
            'empleado', 'employee', 'salario', 'salary', 'sueldo', 'wage',
            'departamento', 'department', 'cargo', 'position', 'puesto', 'job',
            'contrato', 'contract', 'fecha_ingreso', 'hire_date', 'antiguedad',
            'benefits', 'beneficios', 'vacaciones', 'ausencia', 'nomina', 'payroll'
        ],
        'inventario': [
            'sku', 'producto', 'product', 'stock', 'existencia', 'cantidad',
            'quantity', 'proveedor', 'supplier', 'almacen', 'warehouse', 'ubicacion',
            'location', 'lote', 'batch', 'serie', 'serial', 'entrada', 'salida',
            'reorden', 'reorder', 'minimo', 'maximo'
        ],
        'marketing': [
            'campaña', 'campaign', 'click', 'impression', 'conversion', 'ctr',
            'cpc', 'cpm', 'roi', 'lead', 'anuncio', 'ad', 'keyword', 'palabra_clave',
            'bounce', 'rebote', 'session', 'sesion', 'pageview', 'usuario', 'user',
            'engagement', 'reach', 'alcance'
        ],
        'salud': [
            'paciente', 'patient', 'diagnostico', 'diagnosis', 'tratamiento',
            'treatment', 'sintoma', 'symptom', 'medicamento', 'medication',
            'doctor', 'medico', 'enfermera', 'nurse', 'cita', 'appointment',
            'historia_clinica', 'expediente', 'analisis', 'test', 'resultado'
        ],
        'logistica': [
            'envio', 'shipment', 'tracking', 'rastreo', 'transportista', 'carrier',
            'destino', 'destination', 'origen', 'origin', 'ruta', 'route',
            'entrega', 'delivery', 'paquete', 'package', 'peso', 'weight',
            'dimension', 'costo_envio', 'shipping_cost', 'tiempo_entrega'
        ]
    }
    
    def __init__(self):
        """Inicializa el extractor"""
        self.feature_names = []
        
    def extract_features(self, df: pd.DataFrame, filename: str = "") -> np.ndarray:
        """
        Extrae vector de features de un DataFrame
        
        Args:
            df: DataFrame a analizar
            filename: Nombre del archivo (opcional)
            
        Returns:
            Array numpy con features extraídas
        """
        features = []
        
        # 1. Features básicas de estructura
        features.extend(self._extract_structure_features(df))
        
        # 2. Features de tipos de datos
        features.extend(self._extract_datatype_features(df))
        
        # 3. Features de nombres de columnas
        features.extend(self._extract_column_name_features(df))
        
        # 4. Features estadísticas
        features.extend(self._extract_statistical_features(df))
        
        # 5. Features de patrones de datos
        features.extend(self._extract_pattern_features(df))
        
        # 6. Features de keywords por dominio
        features.extend(self._extract_keyword_features(df))
        
        return np.array(features, dtype=np.float32)
    
    def _extract_structure_features(self, df: pd.DataFrame) -> List[float]:
        """Features básicas de estructura del DataFrame"""
        return [
            float(len(df)),                    # Número de filas
            float(len(df.columns)),            # Número de columnas
            float(len(df)) / float(len(df.columns)) if len(df.columns) > 0 else 0,  # Ratio filas/columnas
            float(df.isnull().sum().sum()),    # Total de valores nulos
            float(df.isnull().sum().sum()) / (len(df) * len(df.columns)) if len(df) * len(df.columns) > 0 else 0,  # % nulos
        ]
    
    def _extract_datatype_features(self, df: pd.DataFrame) -> List[float]:
        """Features sobre tipos de datos"""
        total_cols = len(df.columns)
        if total_cols == 0:
            return [0.0] * 6
            
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        object_cols = len(df.select_dtypes(include=['object']).columns)
        datetime_cols = len(df.select_dtypes(include=['datetime64']).columns)
        
        return [
            float(numeric_cols) / total_cols,              # % columnas numéricas
            float(object_cols) / total_cols,               # % columnas de texto
            float(datetime_cols) / total_cols,             # % columnas de fecha
            float(numeric_cols),                           # Cantidad absoluta numéricas
            float(object_cols),                            # Cantidad absoluta texto
            float(datetime_cols),                          # Cantidad absoluta fechas
        ]
    
    def _extract_column_name_features(self, df: pd.DataFrame) -> List[float]:
        """Features extraídas de nombres de columnas"""
        if len(df.columns) == 0:
            return [0.0] * 5
            
        col_names = [str(col).lower() for col in df.columns]
        
        # Longitud promedio de nombres
        avg_length = np.mean([len(name) for name in col_names])
        
        # Presencia de underscores/guiones
        has_underscore = sum('_' in name for name in col_names) / len(col_names)
        has_hyphen = sum('-' in name for name in col_names) / len(col_names)
        
        # Presencia de números en nombres
        has_numbers = sum(any(c.isdigit() for c in name) for name in col_names) / len(col_names)
        
        # Longitud promedio de palabras
        words = ' '.join(col_names).split()
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        
        return [
            float(avg_length),
            float(has_underscore),
            float(has_hyphen),
            float(has_numbers),
            float(avg_word_length)
        ]
    
    def _extract_statistical_features(self, df: pd.DataFrame) -> List[float]:
        """Features estadísticas de columnas numéricas"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return [0.0] * 10
        
        features = []
        
        # Media de medias, medianas, desviaciones estándar
        try:
            features.append(float(numeric_df.mean().mean()))
            features.append(float(numeric_df.median().median()))
            features.append(float(numeric_df.std().mean()))
            features.append(float(numeric_df.min().min()))
            features.append(float(numeric_df.max().max()))
            
            # Coeficiente de variación promedio
            cv = (numeric_df.std() / numeric_df.mean()).replace([np.inf, -np.inf], 0).fillna(0)
            features.append(float(cv.mean()))
            
            # Skewness y kurtosis promedio
            features.append(float(numeric_df.skew().mean()))
            features.append(float(numeric_df.kurtosis().mean()))
            
            # Rango promedio
            ranges = numeric_df.max() - numeric_df.min()
            features.append(float(ranges.mean()))
            
            # Porcentaje de valores únicos promedio
            unique_ratios = [len(numeric_df[col].unique()) / len(numeric_df) 
                           for col in numeric_df.columns if len(numeric_df) > 0]
            features.append(float(np.mean(unique_ratios)) if unique_ratios else 0.0)
            
        except Exception as e:
            # Si hay error en cálculos, rellenar con ceros
            features = [0.0] * 10
        
        return features
    
    def _extract_pattern_features(self, df: pd.DataFrame) -> List[float]:
        """Detecta patrones específicos en los datos"""
        features = []
        
        # Detección de fechas en columnas de texto
        date_pattern = r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}'
        date_cols = 0
        for col in df.select_dtypes(include=['object']).columns:
            sample = df[col].dropna().astype(str).head(100)
            if any(re.search(date_pattern, str(val)) for val in sample):
                date_cols += 1
        features.append(float(date_cols) / len(df.columns) if len(df.columns) > 0 else 0)
        
        # Detección de monedas
        currency_pattern = r'[$€£¥₹]|\b(USD|EUR|GBP|JPY)\b'
        currency_cols = 0
        for col in df.select_dtypes(include=['object']).columns:
            sample = df[col].dropna().astype(str).head(100)
            if any(re.search(currency_pattern, str(val), re.IGNORECASE) for val in sample):
                currency_cols += 1
        features.append(float(currency_cols) / len(df.columns) if len(df.columns) > 0 else 0)
        
        # Detección de IDs (columnas con valores únicos secuenciales)
        id_cols = 0
        for col in df.select_dtypes(include=[np.number]).columns:
            unique_ratio = len(df[col].unique()) / len(df) if len(df) > 0 else 0
            if unique_ratio > 0.95:  # Más del 95% valores únicos
                id_cols += 1
        features.append(float(id_cols) / len(df.columns) if len(df.columns) > 0 else 0)
        
        # Detección de emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_cols = 0
        for col in df.select_dtypes(include=['object']).columns:
            sample = df[col].dropna().astype(str).head(100)
            if any(re.search(email_pattern, str(val)) for val in sample):
                email_cols += 1
        features.append(float(email_cols) / len(df.columns) if len(df.columns) > 0 else 0)
        
        # Detección de URLs
        url_pattern = r'https?://\S+|www\.\S+'
        url_cols = 0
        for col in df.select_dtypes(include=['object']).columns:
            sample = df[col].dropna().astype(str).head(100)
            if any(re.search(url_pattern, str(val)) for val in sample):
                url_cols += 1
        features.append(float(url_cols) / len(df.columns) if len(df.columns) > 0 else 0)
        
        return features
    
    def _extract_keyword_features(self, df: pd.DataFrame) -> List[float]:
        """
        Features basadas en presencia de keywords específicas por dominio
        Retorna un score por cada categoría
        """
        features = []
        
        # Obtener todo el texto: nombres de columnas + muestra de valores
        text_content = ' '.join([str(col).lower() for col in df.columns])
        
        # Agregar muestra de valores de texto (primeras 100 filas)
        for col in df.select_dtypes(include=['object']).columns:
            sample_values = df[col].dropna().head(100).astype(str).str.lower()
            text_content += ' ' + ' '.join(sample_values)
        
        # Calcular score para cada categoría
        for category, keywords in self.DOMAIN_KEYWORDS.items():
            matches = sum(1 for keyword in keywords if keyword in text_content)
            score = float(matches) / len(keywords) if keywords else 0.0
            features.append(score)
        
        return features
    
    def get_feature_names(self) -> List[str]:
        """Retorna nombres descriptivos de las features"""
        names = [
            # Estructura
            'n_rows', 'n_cols', 'row_col_ratio', 'total_nulls', 'null_percentage',
            
            # Tipos de datos
            'pct_numeric_cols', 'pct_object_cols', 'pct_datetime_cols',
            'abs_numeric_cols', 'abs_object_cols', 'abs_datetime_cols',
            
            # Nombres de columnas
            'avg_col_name_length', 'pct_underscore', 'pct_hyphen', 
            'pct_numbers_in_names', 'avg_word_length',
            
            # Estadísticas
            'mean_of_means', 'median_of_medians', 'mean_std', 'global_min', 
            'global_max', 'mean_cv', 'mean_skewness', 'mean_kurtosis',
            'mean_range', 'mean_unique_ratio',
            
            # Patrones
            'pct_date_cols', 'pct_currency_cols', 'pct_id_cols', 
            'pct_email_cols', 'pct_url_cols',
        ]
        
        # Keywords por categoría
        for category in self.DOMAIN_KEYWORDS.keys():
            names.append(f'keyword_score_{category}')
        
        self.feature_names = names
        return names


def test_extractor():
    """Función de prueba"""
    # Crear CSV de ejemplo - Finanzas
    df_finance = pd.DataFrame({
        'fecha_transaccion': pd.date_range('2024-01-01', periods=100),
        'monto': np.random.uniform(10, 1000, 100),
        'tipo': np.random.choice(['ingreso', 'gasto'], 100),
        'categoria': np.random.choice(['ventas', 'servicios', 'otros'], 100),
        'cuenta': [f'ACC{i:04d}' for i in range(100)]
    })
    
    # Crear CSV de ejemplo - Educación
    df_education = pd.DataFrame({
        'alumno': [f'Estudiante_{i}' for i in range(100)],
        'materia': np.random.choice(['Matemáticas', 'Historia', 'Ciencias'], 100),
        'calificacion': np.random.uniform(0, 100, 100),
        'asistencia': np.random.uniform(70, 100, 100),
        'profesor': np.random.choice(['Prof. A', 'Prof. B', 'Prof. C'], 100)
    })
    
    extractor = CSVFeatureExtractor()
    
    print("=== Features de CSV Financiero ===")
    features_finance = extractor.extract_features(df_finance)
    print(f"Shape: {features_finance.shape}")
    print(f"Features: {features_finance[:10]}...")  # Primeras 10
    
    print("\n=== Features de CSV Educativo ===")
    features_edu = extractor.extract_features(df_education)
    print(f"Shape: {features_edu.shape}")
    print(f"Features: {features_edu[:10]}...")
    
    print("\n=== Nombres de Features ===")
    feature_names = extractor.get_feature_names()
    print(f"Total features: {len(feature_names)}")
    print("Primeras 15:")
    for i, name in enumerate(feature_names[:15], 1):
        print(f"  {i}. {name}")


if __name__ == "__main__":
    test_extractor()
