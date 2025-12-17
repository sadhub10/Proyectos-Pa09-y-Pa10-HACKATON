import time
import threading
from machine import Pin, PWM, UART
from collections import deque
import json

# ============================================================================
# CONFIGURACIÓN GENERAL
# ============================================================================

class SystemConfig:
    """Configuración centralizada del sistema"""
    # Umbrales
    YOLO_CONFIDENCE_THRESHOLD = 0.6
    ULTRASONIC_DISTANCE_THRESHOLD = 1.0  # metros (cercano)
    COLLISION_DISTANCE_THRESHOLD = 0.3    # metros (muy cercano)
    ULTRASONIC_SUSTAIN_TIME = 3.0         # segundos para confirmar
    
    # Hardware
    ULTRASONIC_FRONT_TRIG = 16
    ULTRASONIC_FRONT_ECHO = 17
    ULTRASONIC_CANE_TRIG = 18
    ULTRASONIC_CANE_ECHO = 19
    BUTTON_POWER = 20
    BUTTON_MUTE = 21
    SPEAKER_LEFT = 12
    SPEAKER_RIGHT = 13
    
    # Tiempos
    LOOP_DELAY = 0.1  # 100ms entre ciclos
    FRAME_CAPTURE_TIME = 0.05  # capturar frame cada 50ms


# ============================================================================
# CLASE: GESTIÓN DE SENSORES ULTRASÓNICOS
# ============================================================================

class UltrasonicSensor:
    """Controla sensores ultrasónicos HC-SR04"""
    
    def __init__(self, trig_pin, echo_pin, name="Sensor"):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.name = name
        self.last_distance = None
        
    def measure_distance(self):
        """Mide distancia en metros (máx 4m)"""
        try:
            self.trig.off()
            time.sleep_us(2)
            self.trig.on()
            time.sleep_us(10)
            self.trig.off()
            
            # Esperar flanco de subida
            timeout = time.ticks_ms()
            while self.echo.value() == 0:
                if time.ticks_ms() - timeout > 100:
                    return None
            
            start = time.ticks_us()
            
            # Esperar flanco de bajada
            timeout = time.ticks_ms()
            while self.echo.value() == 1:
                if time.ticks_ms() - timeout > 100:
                    return None
            
            end = time.ticks_us()
            
            # Calcular distancia: velocidad del sonido = 343 m/s
            pulse_duration = end - start
            distance = (pulse_duration / 2) / 29.1  # cm
            distance_m = distance / 100  # metros
            
            self.last_distance = distance_m
            return distance_m
        except:
            return None


class SensorDetectionHistory:
    """Almacena historial de detecciones ultrasónicas"""
    
    def __init__(self, max_time=5.0):
        self.max_time = max_time
        self.detections = deque()  # (timestamp, distance)
        
    def add_detection(self, distance):
        """Agrega detección al historial"""
        current_time = time.time()
        self.detections.append((current_time, distance))
        
        # Limpiar detecciones antiguas
        while self.detections and self.detections[0][0] < current_time - self.max_time:
            self.detections.popleft()
    
    def check_sustained_detection(self, threshold_distance, sustain_time):
        """Verifica si hay detección sostenida en tiempo especificado"""
        if not self.detections:
            return False
        
        current_time = time.time()
        sustained_count = 0
        
        for timestamp, distance in self.detections:
            if distance < threshold_distance and (current_time - timestamp) <= sustain_time:
                sustained_count += 1
        
        return sustained_count >= 3  # Al menos 3 detecciones en el rango


# ============================================================================
# CLASE: DETECCIÓN VISUAL (YOLO + CÁLCULOS)
# ============================================================================

class CameraDetector:
    """Simula detección de cámara con YOLO"""
    
    def __init__(self):
        self.current_detections = []
        self.last_detections = []
        self.detection_timestamp = time.time()
        
    def simulate_yolo_detection(self):
        """
        Simula detección YOLO
        En hardware real, aquí irían frames de la cámara
        """
        # Simulación: objetos detectados con confianza
        simulated_objects = [
            {
                'class': 'escalera',
                'confidence': 0.85,
                'bbox': [100, 50, 200, 300],  # x1, y1, x2, y2
                'position': 'frente'
            },
            {
                'class': 'persona',
                'confidence': 0.92,
                'bbox': [300, 100, 400, 400],
                'position': 'derecha'
            }
        ]
        
        return simulated_objects
    
    def filter_by_confidence(self, detections, threshold):
        """Filtra detecciones por umbral de confianza"""
        return [d for d in detections if d['confidence'] >= threshold]
    
    def calculate_distance_from_bbox(self, bbox):
        """
        Calcula distancia usando bounding box
        En hardware real, usaría MiDaS o sensor de profundidad
        
        Aproximación: mayor bbox = más cercano
        """
        x1, y1, x2, y2 = bbox
        bbox_size = (x2 - x1) * (y2 - y1)
        
        # Simulación de conversión a metros
        # (en realidad usaría modelo de profundidad)
        if bbox_size > 30000:
            distance = 0.5  # muy cercano
        elif bbox_size > 15000:
            distance = 1.0
        elif bbox_size > 5000:
            distance = 2.0
        else:
            distance = 3.5
        
        return distance
    
    def determine_position(self, bbox, frame_width=640, frame_height=480):
        """Determina posición: izquierda, derecha, frente, diagonal"""
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Dividir pantalla en 9 zonas
        third_width = frame_width / 3
        third_height = frame_height / 3
        
        if center_x < third_width:
            horizontal = "izquierda"
        elif center_x < 2 * third_width:
            horizontal = "frente"
        else:
            horizontal = "derecha"
        
        if center_y < third_height:
            vertical = "arriba"
        elif center_y < 2 * third_height:
            vertical = "centro"
        else:
            vertical = "abajo"
        
        if horizontal == "frente" and vertical == "centro":
            return "frente"
        else:
            return f"{vertical}-{horizontal}"
    
    def generate_natural_language(self, detections):
        """Genera texto natural a partir de detecciones"""
        if not detections:
            return "No hay objetos detectados"
        
        texts = []
        for det in detections:
            class_name = det['class']
            distance = det['distance']
            position = det['position']
            
            # Clasificar distancia
            if distance < 0.5:
                distance_text = "muy cerca"
            elif distance < 1.5:
                distance_text = "cerca"
            else:
                distance_text = "lejos"
            
            # Generar frase
            text = f"{class_name} {distance_text} a {distance:.1f} metros en tu {position}"
            texts.append(text)
        
        return ". ".join(texts)


# ============================================================================
# CLASE: GESTOR DE AUDIO Y ALERTAS
# ============================================================================

class AudioManager:
    """Maneja reproducción de audio y alertas"""
    
    def __init__(self, speaker_left_pin, speaker_right_pin):
        self.speaker_left = PWM(Pin(speaker_left_pin))
        self.speaker_right = PWM(Pin(speaker_right_pin))
        self.muted = False
        self.current_frequency = 1000
        
    def set_mute(self, muted):
        """Activa/desactiva mute"""
        self.muted = muted
    
    def play_alert_tone(self, frequency=1000, duration=0.5):
        """Reproduce tono de alerta"""
        if self.muted:
            return
        
        self.speaker_left.freq(frequency)
        self.speaker_left.duty_u16(32768)  # 50% duty cycle
        
        self.speaker_right.freq(frequency)
        self.speaker_right.duty_u16(32768)
        
        time.sleep(duration)
        
        self.speaker_left.duty_u16(0)
        self.speaker_right.duty_u16(0)
    
    def play_speech_simulation(self, text):
        """
        Simula reproducción de voz
        En hardware real, usaría pyttsx3 o Google Text-to-Speech
        """
        if self.muted:
            return
        
        print(f"🔊 AUDIO GENERADO: {text}")
        
        # Simular sonido reproduciendo tonos
        frequencies = [800, 1000, 1200]
        for freq in frequencies:
            self.play_alert_tone(frequency=freq, duration=0.1)
    
    def play_collision_alert(self):
        """Alerta de colisión inminente - frecuencia urgente"""
        if self.muted:
            return
        
        print("🚨 ¡¡¡ALERTA CRÍTICA!!!")
        
        # Patrón: dos tonos rápidos
        for _ in range(3):
            self.play_alert_tone(frequency=2000, duration=0.2)
            time.sleep(0.1)


# ============================================================================
# CLASE: CONTROLADOR PRINCIPAL
# ============================================================================

class BlindAssistantController:
    """Controlador principal del sistema"""
    
    def __init__(self):
        self.power_on = False
        self.config = SystemConfig()
        
        # Sensores ultrasónicos
        self.ultrasonic_front = UltrasonicSensor(
            self.config.ULTRASONIC_FRONT_TRIG,
            self.config.ULTRASONIC_FRONT_ECHO,
            "Frontal"
        )
        self.ultrasonic_cane = UltrasonicSensor(
            self.config.ULTRASONIC_CANE_TRIG,
            self.config.ULTRASONIC_CANE_ECHO,
            "Bastón"
        )
        
        self.sensor_history_front = SensorDetectionHistory()
        self.sensor_history_cane = SensorDetectionHistory()
        
        # Cámara
        self.camera = CameraDetector()
        
        # Audio
        self.audio = AudioManager(
            self.config.SPEAKER_LEFT,
            self.config.SPEAKER_RIGHT
        )
        
        # Botones
        self.button_power = Pin(self.config.BUTTON_POWER, Pin.IN, Pin.PULL_UP)
        self.button_mute = Pin(self.config.BUTTON_MUTE, Pin.IN, Pin.PULL_UP)
        
        # Callbacks
        self.button_power.irq(trigger=Pin.IRQ_FALLING, handler=self.on_power_button)
        self.button_mute.irq(trigger=Pin.IRQ_FALLING, handler=self.on_mute_button)
        
        # Threads
        self.cam_thread = None
        self.sensor_thread = None
        self.running = False
        
        print("Sistema inicializado correctamente")
    
    def on_power_button(self, pin):
        """Callback: Botón de encendido"""
        time.sleep(0.2)  # Debounce
        self.power_on = not self.power_on
        
        if self.power_on:
            print("🟢 SISTEMA ENCENDIDO")
            print("⚙️ Energizando: Raspberry Pi, Bocinas, Sensores")
            self.start_system()
        else:
            print("🔴 SISTEMA APAGADO")
            self.stop_system()
    
    def on_mute_button(self, pin):
        """Callback: Botón de mute"""
        time.sleep(0.2)  # Debounce
        muted = not self.audio.muted
        self.audio.set_mute(muted)
        status = "SILENCIADO" if muted else "SONIDO ACTIVADO"
        print(f"🔇 {status}")
    
    def start_system(self):
        """Inicia threads de sensores y cámara"""
        self.running = True
        
        # Thread para cámara YOLO
        self.cam_thread = threading.Thread(target=self.cam_detect_loop, daemon=True)
        self.cam_thread.start()
        
        # Thread para sensores ultrasónicos
        self.sensor_thread = threading.Thread(target=self.sensors_detect_loop, daemon=True)
        self.sensor_thread.start()
    
    def stop_system(self):
        """Detiene todos los threads"""
        self.running = False
        time.sleep(0.5)
    
    # ========================================================================
    # FUNCIÓN: CAM_DETECT (Rama de Visión)
    # ========================================================================
    
    def cam_detect_loop(self):
        """Loop principal de detección visual"""
        print("\n📷 CAM_DETECT: Iniciado")
        print("⏱️ YOLOv11 activado, capturando frames...")
        
        while self.running:
            try:
                # Paso 1: Capturar frame y detectar con YOLO
                detections = self.camera.simulate_yolo_detection()
                
                # Paso 2: Filtrar por confianza
                confident_detections = self.camera.filter_by_confidence(
                    detections,
                    self.config.YOLO_CONFIDENCE_THRESHOLD
                )
                
                if not confident_detections:
                    time.sleep(self.config.LOOP_DELAY)
                    continue
                
                print(f"\n✅ Objetos detectados: {len(confident_detections)}")
                
                # Paso 3: Calcular distancia y posición
                for detection in confident_detections:
                    bbox = detection['bbox']
                    detection['distance'] = self.camera.calculate_distance_from_bbox(bbox)
                    detection['position'] = self.camera.determine_position(bbox)
                
                # Paso 4: Generar lenguaje natural
                natural_text = self.camera.generate_natural_language(confident_detections)
                
                # Paso 5: Comparar con detecciones anteriores
                should_alert, is_collision = self._evaluate_detections(confident_detections)
                
                if should_alert:
                    # Paso 6: Activar función de reproducción
                    self._activate_audio_output(natural_text, is_collision)
                
                self.camera.last_detections = confident_detections
                time.sleep(self.config.LOOP_DELAY)
                
            except Exception as e:
                print(f"Error en CAM_DETECT: {e}")
                time.sleep(self.config.LOOP_DELAY)
    
    def _evaluate_detections(self, current_detections):
        """
        Compara detecciones actuales con las anteriores
        Retorna tupla: (should_alert, is_collision)
        """
        if not self.camera.last_detections:
            # Primera detección: verificar si es colisión
            for detection in current_detections:
                if detection['distance'] < self.config.COLLISION_DISTANCE_THRESHOLD:
                    return True, True
            return False, False
        
        # Obtener clases actuales y anteriores
        current_classes = set(d['class'] for d in current_detections)
        last_classes = set(d['class'] for d in self.camera.last_detections)
        
        # Si hay nuevos objetos (diferentes) -> ALERTA CRÍTICA
        if current_classes != last_classes:
            return True, True
        
        # Si los objetos son iguales, verificar distancia
        for curr in current_detections:
            for last in self.camera.last_detections:
                if curr['class'] == last['class']:
                    # Se acerca
                    if curr['distance'] < last['distance']:
                        # Verificar si es colisión inminente
                        if curr['distance'] < self.config.COLLISION_DISTANCE_THRESHOLD:
                            return True, True  # Alerta crítica
                        else:
                            return False, False  # Distancia normal, no alertar
        
        return False, False
    
    def _activate_audio_output(self, text, is_collision=False):
        """Activa reproducción de audio si no está muteado"""
        if self.audio.muted:
            return
        
        if is_collision:
            print(f"\n🚨 ALERTA CRÍTICA: {text}")
            self.audio.play_collision_alert()
        else:
            print(f"\n🔊 REPRODUCIENDO: {text}")
            self.audio.play_speech_simulation(text)
    
    # ========================================================================
    # FUNCIÓN: SENSORS_DETECT (Rama de Sensores)
    # ========================================================================
    
    def sensors_detect_loop(self):
        """Loop principal de detección ultrasónica"""
        print("\n📡 SENSORS_DETECT: Iniciado")
        print("🔊 Sensores ultrasónicos activos (frente + bastón)...\n")
        
        while self.running:
            try:
                # Paso 1: Leer ambos sensores
                distance_front = self.ultrasonic_front.measure_distance()
                distance_cane = self.ultrasonic_cane.measure_distance()
                
                # Paso 2: Guardar en historial si está debajo del umbral
                if distance_front and distance_front < self.config.ULTRASONIC_DISTANCE_THRESHOLD:
                    self.sensor_history_front.add_detection(distance_front)
                
                if distance_cane and distance_cane < self.config.ULTRASONIC_DISTANCE_THRESHOLD:
                    self.sensor_history_cane.add_detection(distance_cane)
                
                # Paso 3: Revisar si hay detección sostenida en sensor frontal
                sustained_front = self.sensor_history_front.check_sustained_detection(
                    self.config.ULTRASONIC_DISTANCE_THRESHOLD,
                    self.config.ULTRASONIC_SUSTAIN_TIME
                )
                
                # Paso 4: Revisar si hay detección sostenida en sensor del bastón
                sustained_cane = self.sensor_history_cane.check_sustained_detection(
                    self.config.ULTRASONIC_DISTANCE_THRESHOLD,
                    self.config.ULTRASONIC_SUSTAIN_TIME
                )
                
                # Paso 5: Si hay detección sostenida, alertar
                if sustained_front:
                    self._handle_sustained_sensor_alert(
                        distance_front,
                        "sensor frontal"
                    )
                
                if sustained_cane:
                    self._handle_sustained_sensor_alert(
                        distance_cane,
                        "sensor de bastón"
                    )
                
                time.sleep(self.config.LOOP_DELAY)
                
            except Exception as e:
                print(f"Error en SENSORS_DETECT: {e}")
                time.sleep(self.config.LOOP_DELAY)
    
    def _handle_sustained_sensor_alert(self, distance, sensor_name):
        """Maneja alerta de detección sostenida"""
        # Verificar si es colisión inminente
        if distance < self.config.COLLISION_DISTANCE_THRESHOLD:
            print(f"🚨 COLISIÓN INMINENTE ({sensor_name}): {distance:.2f}m")
            self.audio.play_collision_alert()
        else:
            text = f"Obstaculo detectado por {sensor_name} a {distance:.2f} metros"
            print(f"⚠️ ALERTA SENSOR: {text}")
            self._activate_audio_output(text)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    print("\n" + "="*70)
    print(" SISTEMA DE ASISTENCIA PARA PERSONAS CIEGAS")
    print(" Plataforma: Raspberry Pi Pico W + Wokwi")
    print("="*70 + "\n")
    
    # Crear controlador
    controller = BlindAssistantController()
    
    # Mantener programa ejecutándose
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nSistema terminado")
        controller.stop_system()


if __name__ == "__main__":
    main()