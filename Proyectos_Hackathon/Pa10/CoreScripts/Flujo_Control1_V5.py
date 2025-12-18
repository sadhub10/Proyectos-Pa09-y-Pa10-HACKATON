"""
CAM_DETECT - VERSIÓN CON 3 MODELOS YOLO SINCRONIZADOS CON AUDIO
Sistema que integra tres modelos YOLO: genérico, custom 1 y custom 2
"""

import cv2
import numpy as np
from ultralytics import YOLO
import torch
from PIL import Image
import time
import pyttsx3
from typing import Dict, List
import threading
import queue


# ============================================================================
# CLASE: ESTIMADOR DE PROFUNDIDAD
# ============================================================================

class DepthEstimator:
    """Estima profundidad usando modelo MiDaS"""
    
    def __init__(self, model_type="DPT_Large"):
        print("🔄 Cargando modelo MiDaS...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"📱 Dispositivo: {self.device}")
        
        midas = torch.hub.load("intel-isl/MiDaS", model_type)
        self.model = midas.to(self.device)
        self.model.eval()
        
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        
        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform
        
        print("✅ Modelo MiDaS cargado\n")
    
    def estimate_depth(self, image):
        """Estima mapa de profundidad"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        if isinstance(image, np.ndarray):
            original_size = (image.shape[1], image.shape[0])
        else:
            original_size = image.size
        
        input_batch = self.transform(image).to(self.device)
        
        with torch.no_grad():
            prediction = self.model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=original_size,
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        
        depth_map = prediction.cpu().numpy()
        depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        
        return depth_map
    
    def get_depth_at_bbox(self, depth_map, bbox):
        """Obtiene profundidad promedio dentro del bounding box"""
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        h, w = depth_map.shape
        x1 = max(0, min(x1, w-1))
        y1 = max(0, min(y1, h-1))
        x2 = max(x1+1, min(x2, w))
        y2 = max(y1+1, min(y2, h))
        
        region = depth_map[y1:y2, x1:x2]
        avg_depth = np.mean(region)
        
        return avg_depth / 255.0


# ============================================================================
# CLASE: NOTIFICADOR DE AUDIO CON SINCRONIZACIÓN
# ============================================================================

class YOLOAudioNotifier:
    """Convierte predicciones de YOLO a notificaciones de audio sincronizadas"""
    
    def __init__(self, language='es', rate=150, volume=0.9):
        self.language = language
        self.rate = rate
        self.volume = volume
        self.audio_queue = queue.Queue()
        self.is_speaking = False
        self.is_running = True
        self.pending_tasks = 0
        
        self.audio_thread = threading.Thread(target=self._process_audio_queue, daemon=True)
        self.audio_thread.start()
        print("✅ Thread de audio iniciado")
    
    def format_prediction(self, obj: str, distance: float, position: str, 
                         distance_status: str = "") -> str:
        """Formatea la predicción en texto natural"""
        position_map = {
            'arriba': 'en la parte superior',
            'abajo': 'en la parte inferior',
            'izquierda': 'a la izquierda',
            'derecha': 'a la derecha',
            'frente': 'al frente',
            'centro': 'al centro',
            'arriba-izquierda': 'arriba a la izquierda',
            'arriba-derecha': 'arriba a la derecha',
            'arriba-centro': 'arriba al centro',
            'medio-izquierda': 'a la izquierda',
            'medio-derecha': 'a la derecha',
            'abajo-izquierda': 'abajo a la izquierda',
            'abajo-derecha': 'abajo a la derecha',
            'abajo-centro': 'abajo al centro'
        }
        
        pos_text = position_map.get(position.lower(), position)
        
        if distance_status == "muy cerca":
            text = f"¡Alerta! {obj} muy cerca, {pos_text}, a {distance:.1f} metros"
        elif distance_status == "cerca":
            text = f"Atención, {obj} cerca, {pos_text}, a {distance:.1f} metros"
        else:
            text = f"{obj} detectado {pos_text}, a {distance:.1f} metros"
        
        return text
    
    def speak(self, text: str, blocking: bool = False):
        """Encola texto para ser hablado"""
        task = {'type': 'speak', 'text': text}
        self.pending_tasks += 1
        self.audio_queue.put(task)
        
        if blocking:
            while not self.audio_queue.empty() or self.is_speaking:
                time.sleep(0.1)
    
    def _process_audio_queue(self):
        """Procesa cola de audio en thread separado"""
        while self.is_running:
            try:
                task = self.audio_queue.get(timeout=1)
                self.is_speaking = True
                
                engine = pyttsx3.init()
                engine.setProperty('rate', self.rate)
                engine.setProperty('volume', self.volume)
                
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
                
                if task['type'] == 'speak':
                    engine.say(task['text'])
                    engine.runAndWait()
                
                del engine
                
                self.is_speaking = False
                self.pending_tasks = max(0, self.pending_tasks - 1)
                self.audio_queue.task_done()
                
            except queue.Empty:
                self.is_speaking = False
                continue
            except Exception as e:
                print(f"Error procesando audio: {e}")
                self.is_speaking = False
                self.pending_tasks = max(0, self.pending_tasks - 1)
    
    def notify_detection(self, prediction: Dict, blocking: bool = False):
        """Notifica una detección de YOLO"""
        text = self.format_prediction(
            obj=prediction.get('objeto', 'Objeto'),
            distance=prediction.get('distancia', 0.0),
            position=prediction.get('posicion', 'centro'),
            distance_status=prediction.get('estado_distancia', '')
        )
        
        self.speak(text, blocking)
    
    def is_busy(self):
        """Verifica si está ocupado procesando audio"""
        return self.is_speaking or self.pending_tasks > 0 or not self.audio_queue.empty()
    
    def wait_until_done(self):
        """Espera hasta que se procesen todas las tareas pendientes"""
        self.audio_queue.join()
        while self.is_speaking or self.pending_tasks > 0:
            time.sleep(0.1)
    
    def shutdown(self):
        """Detiene el notificador de forma segura"""
        self.is_running = False
        if self.audio_thread.is_alive():
            self.audio_thread.join(timeout=2)


# ============================================================================
# CLASE: TRIPLE CAM_DETECT - CON TRES MODELOS YOLO SINCRONIZADO
# ============================================================================

class TripleCAMDetect:
    """Sistema de detección con TRES modelos YOLO sincronizado con audio"""
    
    def __init__(self, 
                 generic_model="yolo11n.pt", 
                 custom_model_1=r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V72\weights\best.pt",
                 custom_model_2=r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V7\weights\Gabrielbest.pt",
                 midas_type="DPT_Large"):
        """
        Inicializa detector con TRES modelos YOLO
        
        Args:
            generic_model: Modelo YOLO genérico (80 clases COCO)
            custom_model_1: Tu primer modelo personalizado
            custom_model_2: Tu segundo modelo personalizado
            midas_type: Tipo de modelo MiDaS
        """
        print("="*70)
        print(" TRIPLE CAM_DETECT - SISTEMA CON TRES MODELOS YOLO")
        print("="*70 + "\n")
        
        # Configuración
        self.config = {
            'YOLO_CONFIDENCE_THRESHOLD': 0.6,
            'COLLISION_DISTANCE_THRESHOLD': 0.3,
            'DISTANCE_SCALE': 2.0,
            'FRAME_WIDTH': 640,
            'FRAME_HEIGHT': 640,
            'PROCESS_INTERVAL': 0.5
        }
        
        # ========== CARGAR MODELO GENÉRICO ==========
        print(f"🔄 Cargando modelo YOLO GENÉRICO: {generic_model}")
        self.generic_yolo = YOLO(generic_model)
        print(f"✅ Modelo genérico cargado")
        print(f"   - Clases: {len(self.generic_yolo.names)}")
        print(f"   - Ejemplos: {list(self.generic_yolo.names.values())[:5]}...\n")
        
        # ========== CARGAR MODELO PERSONALIZADO 1 ==========
        self.custom_yolo_1 = None
        self.custom_1_name_mapping = {0: "Hole", 2: "None"}  # Mapeo de nombres personalizados
        
        if custom_model_1:
            print(f"🔄 Cargando modelo YOLO PERSONALIZADO 1: {custom_model_1}")
            self.custom_yolo_1 = YOLO(custom_model_1)
            print(f"✅ Modelo personalizado 1 cargado")
            print(f"   - Clases: {len(self.custom_yolo_1.names)}")
            print(f"   - Nombres originales: {list(self.custom_yolo_1.names.values())}")
            print(f"   - Renombrados: {self.custom_1_name_mapping}\n")
        
        # ========== CARGAR MODELO PERSONALIZADO 2 ==========
        self.custom_yolo_2 = None
        if custom_model_2:
            print(f"🔄 Cargando modelo YOLO PERSONALIZADO 2: {custom_model_2}")
            self.custom_yolo_2 = YOLO(custom_model_2)
            print(f"✅ Modelo personalizado 2 cargado")
            print(f"   - Clases: {len(self.custom_yolo_2.names)}")
            print(f"   - Nombres: {list(self.custom_yolo_2.names.values())}\n")
        
        # ========== CARGAR MIDAS Y AUDIO ==========
        self.depth_estimator = DepthEstimator(model_type=midas_type)
        
        print("🔄 Inicializando sistema de audio...")
        self.audio_notifier = YOLOAudioNotifier(language='es', rate=150, volume=0.9)
        print("✅ Sistema de audio inicializado\n")
        
        self.muted = False
        self.last_detections = {}
        self.last_process_time = 0
        
        print("✅ Sistema triple inicializado completamente\n")
    
    def filter_by_confidence(self, detections, threshold):
        """Filtra detecciones por confianza"""
        return [d for d in detections if d['confidence'] >= threshold]
    
    def calculate_distance_from_bbox(self, bbox, depth_map):
        """Calcula distancia del objeto"""
        depth_value = self.depth_estimator.get_depth_at_bbox(depth_map, bbox)
        distance = self.config['DISTANCE_SCALE'] * (1.0 - depth_value) + 0.3
        return distance, depth_value
    
    def determine_position(self, bbox, frame_shape):
        """Determina posición relativa del objeto"""
        h, w = frame_shape[:2]
        x1, y1, x2, y2 = bbox
        
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        third_width = w / 3
        if center_x < third_width:
            horizontal = "izquierda"
        elif center_x < 2 * third_width:
            horizontal = "centro"
        else:
            horizontal = "derecha"
        
        third_height = h / 3
        if center_y < third_height:
            vertical = "arriba"
        elif center_y < 2 * third_height:
            vertical = "medio"
        else:
            vertical = "abajo"
        
        if horizontal == "centro" and vertical == "medio":
            return "frente"
        
        return f"{vertical}-{horizontal}"
    
    def categorize_distance(self, distance):
        """Categoriza distancia"""
        if distance < 0.5:
            return "muy cerca"
        elif distance < 1.5:
            return "cerca"
        elif distance < 3.0:
            return "a distancia normal"
        else:
            return "lejos"
    
    def _simple_nms(self, boxes, scores, iou_threshold=0.5):
        """NMS simple para eliminar detecciones duplicadas"""
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            
            iou = inter / (areas[i] + areas[order[1:]] - inter)
            
            inds = np.where(iou <= iou_threshold)[0]
            order = order[inds + 1]
        
        return keep
    
    def merge_detections(self, detections_generic: List, detections_custom_1: List, 
                        detections_custom_2: List) -> List:
        """Combina detecciones de los TRES modelos, eliminando duplicados"""
        all_detections = detections_generic + detections_custom_1 + detections_custom_2
        
        if len(all_detections) <= 1:
            return all_detections
        
        boxes = []
        scores = []
        indices_map = []
        
        for idx, det in enumerate(all_detections):
            bbox = det['bbox']
            boxes.append([bbox[0], bbox[1], bbox[2], bbox[3]])
            scores.append(det['confidence'])
            indices_map.append(idx)
        
        boxes = np.array(boxes)
        scores = np.array(scores)
        
        keep_indices = self._simple_nms(boxes, scores, iou_threshold=0.5)
        merged = [all_detections[i] for i in keep_indices]
        
        return merged
    
    def process_yolo_results(self, results, model_source="generic"):
        """Procesa resultados de un modelo YOLO"""
        detections = []
        
        if not results or len(results) == 0:
            return detections
        
        result = results[0]
        
        if len(result.boxes) == 0:
            return detections
        
        for box in result.boxes:
            try:
                bbox = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                
                if class_id not in result.names:
                    continue
                
                class_name = result.names[class_id]
                
                # Aplicar renombrado personalizado solo para custom_1
                if model_source == "custom_1" and class_id in self.custom_1_name_mapping:
                    class_name = self.custom_1_name_mapping[class_id]
                
                detection = {
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': bbox,
                    'class_id': class_id,
                    'source': model_source
                }
                detections.append(detection)
                
            except Exception as e:
                print(f"❌ Error procesando detección: {e}")
                continue
        
        return detections
    
    def generate_natural_language(self, detections):
        """Genera lenguaje natural y activa audio SINCRONIZADO"""
        if not detections:
            return None
        
        print(f"\n{'='*70}")
        print(f"✅ DETECCIONES ENCONTRADAS: {len(detections)}")
        print(f"{'='*70}\n")
        
        # Ordenar: primero custom_2, luego custom_1, luego generic
        def sort_key(x):
            if x['source'] == 'custom_2':
                return (0, x['class'])
            elif x['source'] == 'custom_1':
                return (1, x['class'])
            else:
                return (2, x['class'])
        
        detections_sorted = sorted(detections, key=sort_key)
        
        for idx, det in enumerate(detections_sorted, 1):
            class_name = det['class']
            distance = det['distance']
            position = det['position']
            distance_category = self.categorize_distance(distance)
            confidence = det['confidence']
            depth_value = det['depth_value']
            source = det['source']
            
            # Emojis por modelo
            if source == "generic":
                source_emoji = "🌐"
            elif source == "custom_1":
                source_emoji = "⭐"
            else:  # custom_2
                source_emoji = "💎"
            
            print(f"{source_emoji} Objeto {idx} [{source.upper()}]:")
            print(f"   Clase: {class_name}")
            print(f"   Confianza: {confidence:.1%}")
            print(f"   Profundidad (0-1): {depth_value:.3f}")
            print(f"   Distancia estimada: {distance:.2f}m")
            print(f"   Posición: {position}")
            print(f"   Categoría: {distance_category}\n")
            
            if not self.muted:
                prediction_dict = {
                    'objeto': class_name,
                    'distancia': distance,
                    'posicion': position,
                    'estado_distancia': distance_category
                }
                
                self.audio_notifier.notify_detection(prediction_dict, blocking=False)
                print(f"   🔊 Audio encolado: {distance_category}")
        
        print(f"{'='*70}\n")
        
        # ESPERAR a que termine TODO el audio
        if not self.muted and detections:
            print("⏳ Esperando a que termine el audio...")
            self.audio_notifier.wait_until_done()
            print("✅ Audio completado, continuando\n")
        
        return True
    
    def process_frame(self, frame):
        """Procesa frame con los TRES modelos YOLO - SINCRONIZADO"""
        current_time = time.time()
        
        # NO procesar si el audio está ocupado
        if not self.muted and self.audio_notifier.is_busy():
            return frame, None
        
        # Verificar intervalo
        if current_time - self.last_process_time < self.config['PROCESS_INTERVAL']:
            return frame, None
        
        self.last_process_time = current_time
        
        # ========== DETECTAR CON MODELO GENÉRICO ==========
        try:
            results_generic = self.generic_yolo(frame, verbose=False)
            detections_generic = self.process_yolo_results(results_generic, "generic")
        except Exception as e:
            print(f"❌ Error en modelo genérico: {e}")
            detections_generic = []
        
        # ========== DETECTAR CON MODELO PERSONALIZADO 1 ==========
        detections_custom_1 = []
        if self.custom_yolo_1:
            try:
                results_custom_1 = self.custom_yolo_1(frame, verbose=False)
                detections_custom_1 = self.process_yolo_results(results_custom_1, "custom_1")
            except Exception as e:
                print(f"❌ Error en modelo personalizado 1: {e}")
        
        # ========== DETECTAR CON MODELO PERSONALIZADO 2 ==========
        detections_custom_2 = []
        if self.custom_yolo_2:
            try:
                results_custom_2 = self.custom_yolo_2(frame, verbose=False)
                detections_custom_2 = self.process_yolo_results(results_custom_2, "custom_2")
            except Exception as e:
                print(f"❌ Error en modelo personalizado 2: {e}")
        
        # ========== COMBINAR DETECCIONES DE LOS 3 MODELOS ==========
        all_detections = self.merge_detections(
            detections_generic, 
            detections_custom_1, 
            detections_custom_2
        )
        
        if not all_detections:
            return frame, None
        
        # Filtrar por confianza
        valid_detections = self.filter_by_confidence(
            all_detections,
            self.config['YOLO_CONFIDENCE_THRESHOLD']
        )
        
        if not valid_detections:
            return frame, None
        
        # Calcular profundidad
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        depth_map = self.depth_estimator.estimate_depth(frame_rgb)
        
        # Calcular distancia y posición
        for det in valid_detections:
            distance, depth_value = self.calculate_distance_from_bbox(det['bbox'], depth_map)
            position = self.determine_position(det['bbox'], frame.shape)
            
            det['distance'] = distance
            det['depth_value'] = depth_value
            det['position'] = position
        
        # Generar lenguaje natural y audio (BLOQUEA hasta terminar)
        self.generate_natural_language(valid_detections)
        
        # Actualizar historial
        self.last_detections = {
            d['class']: {'distance': d['distance'], 'position': d['position']} 
            for d in valid_detections
        }
        
        # Dibujar en frame
        frame_output = self.draw_detections(frame, valid_detections)
        
        return frame_output, valid_detections, depth_map
    
    def draw_detections(self, frame, detections):
        """Dibuja bounding boxes con colores según modelo"""
        output_frame = frame.copy()
        
        distance_colors = {
            'muy cerca': (0, 0, 255),      # Rojo
            'cerca': (0, 165, 255),         # Naranja
            'a distancia normal': (0, 255, 0),  # Verde
            'lejos': (255, 0, 0)            # Azul
        }
        
        for det in detections:
            bbox = det['bbox']
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            
            distance_category = self.categorize_distance(det['distance'])
            color = distance_colors.get(distance_category, (255, 255, 255))
            
            # Grosor según modelo
            if det['source'] == 'custom_2':
                thickness = 4  # Más grueso para custom_2
            elif det['source'] == 'custom_1':
                thickness = 3
            else:
                thickness = 2
            
            cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, thickness)
            
            # Etiqueta según modelo
            if det['source'] == 'custom_2':
                source_tag = "[💎]"
            elif det['source'] == 'custom_1':
                source_tag = "[★]"
            else:
                source_tag = ""
            
            text = f"{source_tag}{det['class']} ({det['confidence']:.0%}) {det['distance']:.2f}m"
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output_frame, text, (x1, y1 - 10), font, 0.5, color, 2)
        
        return output_frame
    
    def shutdown(self):
        """Cierra el sistema"""
        print("\n🔄 Cerrando sistema de audio...")
        self.audio_notifier.shutdown()
        print("✅ Sistema cerrado correctamente")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def run_triple_webcam_detection(
    generic_model="yolo11n.pt", 
    custom_model_1=r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V72\weights\best.pt",
    custom_model_2=r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V7\weights\Gabrielbest.pt"  # Aquí va la ruta de tu tercer modelo
):
    """Ejecuta detección con TRES modelos SINCRONIZADOS"""
    
    cam_detect = TripleCAMDetect(
        generic_model=generic_model,
        custom_model_1=custom_model_1,
        custom_model_2=custom_model_2,
        midas_type="DPT_Large"
    )
    
    print("\n📹 Abriendo webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ No se pudo abrir la webcam")
        return
    
    print("✅ Webcam abierta")
    print("\n🎮 CONTROLES:")
    print("  - Presiona 'M' para Mute/Sonido")
    print("  - Presiona 'Q' para salir")
    print("\n💡 LEYENDA:")
    print("  - [💎] = Modelo PERSONALIZADO 2 (grosor 4)")
    print("  - [★] = Modelo PERSONALIZADO 1 (grosor 3)")
    print("  - Sin etiqueta = Modelo GENÉRICO (grosor 2)")
    print("\n🔊 MODO SINCRONIZADO:")
    print("  - El sistema espera a que termine el audio")
    print("  - No se acumulan detecciones\n")
    
    last_valid_frame = None
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame = cv2.resize(frame, (cam_detect.config['FRAME_WIDTH'], 
                                       cam_detect.config['FRAME_HEIGHT']))
            
            result = cam_detect.process_frame(frame)
            
            if result is not None and len(result) == 3:
                frame_output, detections, depth_map = result
                last_valid_frame = (frame_output.copy(), depth_map)
            else:
                if last_valid_frame is not None:
                    frame_output, depth_map = last_valid_frame
                else:
                    frame_output = frame
                    depth_map = None
            
            # Indicador visual si está reproduciendo audio
            if not cam_detect.muted and cam_detect.audio_notifier.is_busy():
                cv2.putText(frame_output, "REPRODUCIENDO AUDIO...", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 255), 2)
            
            cv2.imshow("TRIPLE CAM_DETECT - Sincronizado (Q=salir)", frame_output)
            
            if depth_map is not None:
                depth_map_color = cv2.applyColorMap(depth_map, cv2.COLORMAP_VIRIDIS)
                cv2.imshow("Mapa de Profundidad", depth_map_color)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n🛑 Cerrando...")
                break
            elif key == ord('m'):
                cam_detect.muted = not cam_detect.muted
                status = "SILENCIADO 🔇" if cam_detect.muted else "SONIDO ACTIVADO 🔊"
                print(f"\n{status}\n")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        cam_detect.shutdown()
        print("✅ Programa finalizado")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print(" TRIPLE CAM_DETECT - SINCRONIZADO CON AUDIO")
    print(" SISTEMA CON 3 MODELOS YOLO")
    print("="*70 + "\n")
    
    # Modelo genérico
    generic_model = "yolo11n.pt"
    
    # Primer modelo personalizado
    custom_model_1 = r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V72\weights\best.pt"
    
    # Segundo modelo personalizado (CONFIGURA AQUÍ LA RUTA DE TU TERCER MODELO)
    custom_model_2 = r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\Models\IA_Hackaton_V7\weights\Gabrielbest.pt"  # Ejemplo: r"C:\ruta\a\tu\tercer\modelo\best.pt"
    
    # Leer argumentos desde línea de comandos
    if len(sys.argv) > 1:
        custom_model_1 = sys.argv[1]
        print(f"🎯 Usando modelo personalizado 1: {custom_model_1}\n")
    
    if len(sys.argv) > 2:
        custom_model_2 = sys.argv[2]
        print(f"🎯 Usando modelo personalizado 2: {custom_model_2}\n")
    
    # Mostrar configuración
    print("📋 CONFIGURACIÓN DE MODELOS:")
    print(f"   🌐 Genérico: {generic_model}")
    print(f"   ⭐ Custom 1: {custom_model_1}")
    print(f"   💎 Custom 2: {custom_model_2 if custom_model_2 else 'No configurado'}")
    print()
    
    # Ejecutar sistema triple
    run_triple_webcam_detection(
        generic_model=generic_model,
        custom_model_1=custom_model_1,
        custom_model_2=custom_model_2
    )