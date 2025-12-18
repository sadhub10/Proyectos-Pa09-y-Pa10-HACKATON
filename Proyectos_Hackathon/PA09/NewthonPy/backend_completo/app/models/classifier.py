"""
Clasificador de Dominio de CSVs usando Red Neuronal (PyTorch)
Arquitectura: MLP (Multi-Layer Perceptron) entrenada desde cero
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Tuple, Dict
import pickle
import os


class CSVClassifierNN(nn.Module):
    """
    Red Neuronal para clasificación de CSVs por dominio
    Arquitectura: MLP con dropout y batch normalization
    """
    
    def __init__(self, input_size: int, num_classes: int, hidden_sizes: List[int] = None):
        """
        Args:
            input_size: Número de features de entrada
            num_classes: Número de categorías a clasificar
            hidden_sizes: Lista con tamaños de capas ocultas
        """
        super(CSVClassifierNN, self).__init__()
        
        if hidden_sizes is None:
            hidden_sizes = [128, 64, 32]  # Arquitectura por defecto
        
        self.input_size = input_size
        self.num_classes = num_classes
        
        # Construir capas dinámicamente
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            prev_size = hidden_size
        
        # Capa de salida
        layers.append(nn.Linear(prev_size, num_classes))
        
        self.network = nn.Sequential(*layers)
        
        # Inicialización de pesos (Xavier/Glorot)
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Inicializa pesos de la red"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        """Forward pass"""
        return self.network(x)


class CSVDataset(Dataset):
    """Dataset personalizado para PyTorch"""
    
    def __init__(self, features: np.ndarray, labels: np.ndarray):
        """
        Args:
            features: Array de features (n_samples, n_features)
            labels: Array de etiquetas (n_samples,)
        """
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


class CSVClassifier:
    """
    Wrapper para entrenar y usar el clasificador
    """
    
    CATEGORIES = [
        'finanzas',
        'educacion',
        'ventas',
        'rrhh',
        'inventario',
        'marketing',
        'salud',
        'logistica',
        'general'
    ]
    
    def __init__(self, input_size: int, device: str = None):
        """
        Args:
            input_size: Número de features
            device: 'cuda', 'cpu', o None (auto-detect)
        """
        self.input_size = input_size
        self.num_classes = len(self.CATEGORIES)
        
        # Device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        # Modelo
        self.model = CSVClassifierNN(
            input_size=input_size,
            num_classes=self.num_classes,
            hidden_sizes=[128, 64, 32]
        ).to(self.device)
        
        # Métricas
        self.train_losses = []
        self.val_losses = []
        self.val_accuracies = []
    
    def train(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 0.001,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """
        Entrena el modelo
        
        Args:
            X_train: Features de entrenamiento
            y_train: Labels de entrenamiento
            X_val: Features de validación (opcional)
            y_val: Labels de validación (opcional)
            epochs: Número de épocas
            batch_size: Tamaño de batch
            learning_rate: Learning rate
            verbose: Imprimir progreso
            
        Returns:
            Dict con métricas de entrenamiento
        """
        # Datasets
        train_dataset = CSVDataset(X_train, y_train)
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size, 
            shuffle=True,
            num_workers=0
        )
        
        # Loss y optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10, verbose=verbose
        )
        
        # Training loop
        self.model.train()
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            for batch_features, batch_labels in train_loader:
                # Mover a device
                batch_features = batch_features.to(self.device)
                batch_labels = batch_labels.to(self.device)
                
                # Forward
                optimizer.zero_grad()
                outputs = self.model(batch_features)
                loss = criterion(outputs, batch_labels)
                
                # Backward
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(train_loader)
            self.train_losses.append(avg_loss)
            
            # Validación
            if X_val is not None and y_val is not None:
                val_loss, val_acc = self._validate(X_val, y_val, criterion)
                self.val_losses.append(val_loss)
                self.val_accuracies.append(val_acc)
                
                scheduler.step(val_loss)
                
                # Guardar mejor modelo
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.best_model_state = self.model.state_dict().copy()
                
                if verbose and (epoch + 1) % 10 == 0:
                    print(f"Epoch [{epoch+1}/{epochs}] - "
                          f"Train Loss: {avg_loss:.4f} - "
                          f"Val Loss: {val_loss:.4f} - "
                          f"Val Acc: {val_acc:.4f}")
            else:
                if verbose and (epoch + 1) % 10 == 0:
                    print(f"Epoch [{epoch+1}/{epochs}] - Train Loss: {avg_loss:.4f}")
        
        # Restaurar mejor modelo si hay validación
        if X_val is not None and hasattr(self, 'best_model_state'):
            self.model.load_state_dict(self.best_model_state)
        
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'val_accuracies': self.val_accuracies
        }
    
    def _validate(self, X_val: np.ndarray, y_val: np.ndarray, criterion) -> Tuple[float, float]:
        """Evalúa el modelo en conjunto de validación"""
        self.model.eval()
        
        with torch.no_grad():
            val_features = torch.FloatTensor(X_val).to(self.device)
            val_labels = torch.LongTensor(y_val).to(self.device)
            
            outputs = self.model(val_features)
            loss = criterion(outputs, val_labels)
            
            _, predicted = torch.max(outputs, 1)
            accuracy = (predicted == val_labels).float().mean()
        
        self.model.train()
        return loss.item(), accuracy.item()
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predice categorías para nuevos datos
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Array con índices de categorías predichas
        """
        self.model.eval()
        
        with torch.no_grad():
            features = torch.FloatTensor(X).to(self.device)
            outputs = self.model(features)
            _, predicted = torch.max(outputs, 1)
        
        return predicted.cpu().numpy()
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predice probabilidades para cada categoría
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Array con probabilidades (n_samples, n_classes)
        """
        self.model.eval()
        
        with torch.no_grad():
            features = torch.FloatTensor(X).to(self.device)
            outputs = self.model(features)
            probabilities = torch.softmax(outputs, dim=1)
        
        return probabilities.cpu().numpy()
    
    def predict_category(self, X: np.ndarray) -> List[str]:
        """
        Predice categorías como strings
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Lista de nombres de categorías
        """
        predictions = self.predict(X)
        return [self.CATEGORIES[idx] for idx in predictions]
    
    def predict_with_confidence(self, X: np.ndarray) -> List[Tuple[str, float]]:
        """
        Predice categoría con nivel de confianza
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Lista de tuplas (categoría, confianza)
        """
        probas = self.predict_proba(X)
        predictions = []
        
        for proba in probas:
            idx = np.argmax(proba)
            category = self.CATEGORIES[idx]
            confidence = proba[idx]
            predictions.append((category, float(confidence)))
        
        return predictions
    
    def save(self, path: str):
        """Guarda el modelo entrenado"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'input_size': self.input_size,
            'num_classes': self.num_classes,
            'categories': self.CATEGORIES,
            'device': str(self.device)
        }, path)
        
        print(f"Modelo guardado en: {path}")
    
    @classmethod
    def load(cls, path: str, device: str = None):
        """Carga un modelo guardado"""
        checkpoint = torch.load(path, map_location='cpu')
        
        classifier = cls(
            input_size=checkpoint['input_size'],
            device=device
        )
        
        classifier.model.load_state_dict(checkpoint['model_state_dict'])
        classifier.model.eval()
        
        print(f"Modelo cargado desde: {path}")
        return classifier
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evalúa el modelo en conjunto de prueba
        
        Returns:
            Dict con métricas: accuracy, precision, recall, f1
        """
        predictions = self.predict(X_test)
        
        # Accuracy
        accuracy = (predictions == y_test).mean()
        
        # Métricas por clase (micro-average)
        from sklearn.metrics import precision_score, recall_score, f1_score
        
        precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
        recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
        f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
        
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        }


def demo_classifier():
    """Demostración del clasificador"""
    print("=== Demo Clasificador de CSVs ===\n")
    
    # Simular datos de entrenamiento
    np.random.seed(42)
    n_samples = 500
    n_features = 50  # Ajustar según feature_extractor
    
    # Generar features aleatorias
    X = np.random.randn(n_samples, n_features).astype(np.float32)
    
    # Generar labels (9 categorías)
    y = np.random.randint(0, 9, n_samples)
    
    # Split train/test
    split = int(0.8 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Crear y entrenar clasificador
    print("Inicializando clasificador...")
    classifier = CSVClassifier(input_size=n_features)
    
    print(f"Device: {classifier.device}")
    print(f"Arquitectura del modelo:")
    print(classifier.model)
    print()
    
    print("Entrenando modelo (esto puede tardar un poco)...")
    metrics = classifier.train(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        epochs=50,
        batch_size=32,
        learning_rate=0.001,
        verbose=True
    )
    
    # Evaluación
    print("\n=== Evaluación Final ===")
    eval_metrics = classifier.evaluate(X_test, y_test)
    for metric, value in eval_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Predicción de ejemplo
    print("\n=== Predicción de Ejemplo ===")
    sample = X_test[:3]
    predictions = classifier.predict_with_confidence(sample)
    
    for i, (category, confidence) in enumerate(predictions, 1):
        print(f"Muestra {i}: {category} (confianza: {confidence:.2%})")
    
    # Guardar modelo
    print("\n=== Guardando modelo ===")
    classifier.save('/home/claude/backend/data/models/csv_classifier.pth')
    
    print("\nDemo completada")


if __name__ == "__main__":
    demo_classifier()
