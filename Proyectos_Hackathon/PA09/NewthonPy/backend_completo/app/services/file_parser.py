"""
Servicio de Parseo de Archivos
Maneja carga y parseo de CSV, Excel (.xlsx, .xls)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import io
import chardet
from datetime import datetime


class FileParser:
    """Parser inteligente para archivos CSV y Excel"""
    
    SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls', '.tsv', '.txt']
    MAX_FILE_SIZE_MB = 100  # Máximo 100MB
    PREVIEW_ROWS = 10  # Filas para preview
    
    def __init__(self):
        """Inicializa el parser"""
        self.df = None
        self.metadata = {}
    
    def parse_file(
        self, 
        file_path: str = None,
        file_content: bytes = None,
        filename: str = None,
        encoding: str = 'utf-8'
    ) -> pd.DataFrame:
        """
        Parsea un archivo CSV o Excel
        
        Args:
            file_path: Ruta al archivo (opcional)
            file_content: Contenido del archivo en bytes (opcional)
            filename: Nombre del archivo (requerido si se usa file_content)
            encoding: Encoding para CSVs
            
        Returns:
            DataFrame con los datos
            
        Raises:
            ValueError: Si el archivo no es válido
        """
        # Validar inputs
        if file_path is None and file_content is None:
            raise ValueError("Se requiere file_path o file_content")
        
        if file_content is not None and filename is None:
            raise ValueError("Se requiere filename cuando se usa file_content")
        
        # Obtener extensión
        if filename:
            ext = Path(filename).suffix.lower()
        elif file_path:
            ext = Path(file_path).suffix.lower()
            filename = Path(file_path).name
        else:
            raise ValueError("No se pudo determinar el tipo de archivo")
        
        # Validar extensión
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Extensión no soportada: {ext}. "
                f"Soportadas: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Validar tamaño si es contenido en bytes
        if file_content:
            size_mb = len(file_content) / (1024 * 1024)
            if size_mb > self.MAX_FILE_SIZE_MB:
                raise ValueError(
                    f"Archivo muy grande: {size_mb:.1f}MB. "
                    f"Máximo: {self.MAX_FILE_SIZE_MB}MB"
                )
        
        # Parsear según tipo
        try:
            if ext == '.csv':
                df = self._parse_csv(file_path, file_content, encoding)
            elif ext == '.tsv' or ext == '.txt':
                df = self._parse_csv(file_path, file_content, encoding, delimiter='\t')
            elif ext in ['.xlsx', '.xls']:
                df = self._parse_excel(file_path, file_content)
            else:
                raise ValueError(f"Tipo de archivo no soportado: {ext}")
            
            # Validar DataFrame
            if df is None or len(df) == 0:
                raise ValueError("El archivo está vacío o no se pudo leer")
            
            if len(df.columns) == 0:
                raise ValueError("El archivo no tiene columnas")
            
            # Guardar DataFrame y metadata
            self.df = df
            self.metadata = self._extract_metadata(df, filename)
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error parseando archivo: {str(e)}")
    
    def _parse_csv(
        self, 
        file_path: Optional[str] = None,
        file_content: Optional[bytes] = None,
        encoding: str = 'utf-8',
        delimiter: str = ','
    ) -> pd.DataFrame:
        """Parsea archivo CSV"""
        
        # Detectar encoding si es necesario
        if file_content and encoding == 'utf-8':
            detected = chardet.detect(file_content)
            if detected['confidence'] > 0.7:
                encoding = detected['encoding']
        
        # Leer CSV
        if file_path:
            df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
        else:
            df = pd.read_csv(
                io.BytesIO(file_content), 
                encoding=encoding,
                delimiter=delimiter
            )
        
        return df
    
    def _parse_excel(
        self,
        file_path: Optional[str] = None,
        file_content: Optional[bytes] = None
    ) -> pd.DataFrame:
        """Parsea archivo Excel"""
        
        if file_path:
            # Leer primera hoja
            df = pd.read_excel(file_path, sheet_name=0)
        else:
            df = pd.read_excel(io.BytesIO(file_content), sheet_name=0)
        
        return df
    
    def _extract_metadata(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Extrae metadata del DataFrame"""
        
        # Información básica
        metadata = {
            'filename': filename,
            'n_rows': len(df),
            'n_columns': len(df.columns),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'parsed_at': datetime.now().isoformat()
        }
        
        # Información por columna
        column_info = {}
        for col in df.columns:
            col_data = {
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': float(df[col].isnull().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'unique_percentage': float(df[col].nunique() / len(df) * 100)
            }
            
            # Estadísticas para columnas numéricas
            if pd.api.types.is_numeric_dtype(df[col]):
                col_data.update({
                    'min': float(df[col].min()) if not df[col].isnull().all() else None,
                    'max': float(df[col].max()) if not df[col].isnull().all() else None,
                    'mean': float(df[col].mean()) if not df[col].isnull().all() else None,
                    'median': float(df[col].median()) if not df[col].isnull().all() else None,
                    'std': float(df[col].std()) if not df[col].isnull().all() else None
                })
            
            # Valores más frecuentes para columnas categóricas
            if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
                top_values = df[col].value_counts().head(5)
                col_data['top_values'] = {
                    str(k): int(v) for k, v in top_values.items()
                }
            
            column_info[col] = col_data
        
        metadata['column_info'] = column_info
        
        # Detectar posibles problemas
        issues = []
        
        # Columnas con muchos nulos
        high_null_cols = [
            col for col, info in column_info.items() 
            if info['null_percentage'] > 50
        ]
        if high_null_cols:
            issues.append({
                'type': 'high_null_percentage',
                'columns': high_null_cols,
                'message': f"{len(high_null_cols)} columna(s) con >50% valores nulos"
            })
        
        # Columnas con un solo valor
        single_value_cols = [
            col for col, info in column_info.items()
            if info['unique_count'] == 1
        ]
        if single_value_cols:
            issues.append({
                'type': 'single_value',
                'columns': single_value_cols,
                'message': f"{len(single_value_cols)} columna(s) con un solo valor"
            })
        
        # Columnas completamente nulas
        all_null_cols = [
            col for col, info in column_info.items()
            if info['null_count'] == metadata['n_rows']
        ]
        if all_null_cols:
            issues.append({
                'type': 'all_null',
                'columns': all_null_cols,
                'message': f"{len(all_null_cols)} columna(s) completamente vacía(s)"
            })
        
        # Posibles columnas ID (>95% valores únicos)
        possible_id_cols = [
            col for col, info in column_info.items()
            if info['unique_percentage'] > 95
        ]
        if possible_id_cols:
            issues.append({
                'type': 'possible_id_column',
                'columns': possible_id_cols,
                'message': f"{len(possible_id_cols)} posible(s) columna(s) ID detectada(s)"
            })
        
        metadata['issues'] = issues
        
        return metadata
    
    def get_preview(self, n_rows: int = None) -> pd.DataFrame:
        """
        Obtiene preview del DataFrame
        
        Args:
            n_rows: Número de filas (default: PREVIEW_ROWS)
            
        Returns:
            DataFrame con las primeras n_rows
        """
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        if n_rows is None:
            n_rows = self.PREVIEW_ROWS
        
        return self.df.head(n_rows)
    
    def get_sample(self, n_rows: int = 10, random: bool = True) -> pd.DataFrame:
        """
        Obtiene muestra del DataFrame
        
        Args:
            n_rows: Número de filas
            random: Si True, muestra aleatoria. Si False, primeras filas
            
        Returns:
            DataFrame con muestra
        """
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        if random:
            return self.df.sample(min(n_rows, len(self.df)))
        else:
            return self.df.head(n_rows)
    
    def get_column_summary(self, column: str) -> Dict[str, Any]:
        """
        Obtiene resumen detallado de una columna
        
        Args:
            column: Nombre de la columna
            
        Returns:
            Dict con estadísticas de la columna
        """
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        if column not in self.df.columns:
            raise ValueError(f"Columna '{column}' no existe")
        
        return self.metadata['column_info'][column]
    
    def to_dict(self, orient: str = 'records', max_rows: int = None) -> Any:
        """
        Convierte DataFrame a dict
        
        Args:
            orient: Formato ('records', 'list', 'dict', etc.)
            max_rows: Máximo de filas a incluir
            
        Returns:
            Dict con datos
        """
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        df = self.df if max_rows is None else self.df.head(max_rows)
        return df.to_dict(orient=orient)
    
    def get_dtypes_summary(self) -> Dict[str, int]:
        """Resumen de tipos de datos"""
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        dtype_counts = self.df.dtypes.value_counts()
        return {str(dtype): int(count) for dtype, count in dtype_counts.items()}
    
    def detect_date_columns(self) -> List[str]:
        """Detecta columnas que podrían ser fechas"""
        if self.df is None:
            raise ValueError("No hay archivo parseado. Usa parse_file() primero.")
        
        date_columns = []
        
        for col in self.df.select_dtypes(include=['object']).columns:
            # Intentar parsear primeras 10 filas
            sample = self.df[col].dropna().head(10)
            
            try:
                pd.to_datetime(sample, errors='raise')
                date_columns.append(col)
            except:
                continue
        
        return date_columns


def test_parser():
    """Test del parser"""
    print("=== Test FileParser ===\n")
    
    # Crear CSV de prueba
    test_df = pd.DataFrame({
        'id': range(1, 101),
        'nombre': [f'Producto_{i}' for i in range(1, 101)],
        'precio': np.random.uniform(10, 1000, 100),
        'categoria': np.random.choice(['A', 'B', 'C'], 100),
        'fecha': pd.date_range('2024-01-01', periods=100),
        'stock': np.random.randint(0, 100, 100)
    })
    
    # Guardar como CSV
    test_file = '/tmp/test_file.csv'
    test_df.to_csv(test_file, index=False)
    
    # Parsear
    parser = FileParser()
    df = parser.parse_file(test_file)
    
    print(f"✅ Archivo parseado: {len(df)} filas, {len(df.columns)} columnas")
    print(f"\nColumnas: {list(df.columns)}")
    print(f"\nMetadata:")
    print(f"  - Tamaño: {parser.metadata['memory_usage_mb']:.2f} MB")
    print(f"  - Tipos de datos: {parser.get_dtypes_summary()}")
    
    print(f"\n📊 Issues detectados:")
    for issue in parser.metadata['issues']:
        print(f"  - {issue['message']}")
    
    print(f"\n👁️  Preview (primeras 5 filas):")
    print(parser.get_preview(5))
    
    print(f"\n📅 Columnas de fecha detectadas: {parser.detect_date_columns()}")
    
    # Limpiar
    import os
    os.remove(test_file)
    
    print("\n✅ Test completado")


if __name__ == "__main__":
    test_parser()
