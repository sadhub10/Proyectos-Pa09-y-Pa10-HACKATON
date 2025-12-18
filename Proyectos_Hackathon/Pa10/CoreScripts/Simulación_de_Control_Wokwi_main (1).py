"""
Asistente Visual Inteligente para Personas con Discapacidad Visual
Raspberry Pi Pico W - Simulación en Wokwi
Versión Final - Con Simulador de Google Maps API
"""

import time
import random
from machine import Pin, PWM, ADC

print("Iniciando sistema...")

# ==================== CONFIGURACIÓN RASPBERRY PI PICO W ====================
# Botones
BTN_POWER = Pin(15, Pin.IN, Pin.PULL_UP)
BTN_MUTE = Pin(14, Pin.IN, Pin.PULL_UP)
BTN_NAVIGATION = Pin(13, Pin.IN, Pin.PULL_UP)

# Sensores Ultrasónicos
TRIG_BASTON = Pin(2, Pin.OUT)
ECHO_BASTON = Pin(3, Pin.IN)
TRIG_FRENTE = Pin(4, Pin.OUT)
ECHO_FRENTE = Pin(5, Pin.IN)

# Bocinas
SPEAKER_LEFT = PWM(Pin(16))
SPEAKER_RIGHT = PWM(Pin(17))
SPEAKER_LEFT.freq(1000)
SPEAKER_RIGHT.freq(1000)

# LEDs de estado
LED_STATUS = Pin(20, Pin.OUT)
LED_NAVIGATION = Pin(21, Pin.OUT)
LED_DETECTION = Pin(22, Pin.OUT)

# Potenciómetro de selección de destino
POT_VOICE = ADC(Pin(27))

# ==================== VARIABLES GLOBALES ====================
system_on = False
muted = False
navigation_active = False
last_detections = []
current_step_index = 0
distance_to_destination = 0
walking_speed = 4.0  # m/s (AJUSTADO para recorridos de ~13 segundos)
VOLUME = 0.5  # Volumen fijo al 50%
MAX_ROUTE_TIME = 13  # Máximo 13 segundos de recorrido

# Contadores de tiempo
last_camera_check = 0
last_ultrasonic_check = 0
last_navigation_update = 0
last_audio_announcement = 0

# Intervalos de actualización
CAMERA_INTERVAL = 1.0
ULTRASONIC_INTERVAL = 3.0  # Cada 3 segundos (antes 2s)
NAVIGATION_INTERVAL = 1.0  # Cada 1 segundo
AUDIO_INTERVAL = 3.0  # Cada 3 segundos

# Clases de objetos detectables (YOLO)
YOLO_CLASSES = [
    "bolardo", "Borde_de_acera", "cono_seguridad",
    "piso_mojado", "piso_tactil_senal_continuar",
    "piso_tactil_senal_detenerse", "senal_de_piso_mojado"
]

# Umbrales de detección
CONFIDENCE_THRESHOLD = 0.60
PROXIMITY_THRESHOLD = 1.5

# ==================== BASE DE DATOS DE RUTAS SIMULADAS ====================
SIMULATED_ROUTES = {
    "Cafeteria": {
        "start_address": "Universidad Tecnológica de Panamá, Campus",
        "end_address": "Cafetería Central, Campus UTP",
        "distance": {"text": "48 m", "value": 48},
        "duration": {"text": "12 segs", "value": 12},
        "steps": [
            {"instruction": "Sal del edificio hacia el oeste", "distance": 16, "direction": "⬅️ OESTE"},
            {"instruction": "Gira a la derecha hacia la plaza central", "distance": 20, "direction": "➡️ DERECHA"},
            {"instruction": "Continúa recto hasta la cafetería", "distance": 12, "direction": "⬆️ RECTO"},
            {"instruction": "Has llegado a tu destino", "distance": 0, "direction": "🎯 DESTINO"}
        ]
    },
    "Biblioteca": {
        "start_address": "Universidad Tecnológica de Panamá, Campus",
        "end_address": "Biblioteca Dr. Néstor Jaén Barrios",
        "distance": {"text": "52 m", "value": 52},
        "duration": {"text": "13 segs", "value": 13},
        "steps": [
            {"instruction": "Sal del edificio hacia el norte", "distance": 18, "direction": "⬆️ NORTE"},
            {"instruction": "Gira a la izquierda hacia el edificio principal", "distance": 20, "direction": "⬅️ IZQUIERDA"},
            {"instruction": "Sube las escaleras hacia la biblioteca", "distance": 14, "direction": "⬆️ ARRIBA"},
            {"instruction": "Has llegado a la biblioteca", "distance": 0, "direction": "🎯 DESTINO"}
        ]
    },
    "Entrada Principal": {
        "start_address": "Universidad Tecnológica de Panamá, Campus",
        "end_address": "Entrada Principal, Vía Ricardo J. Alfaro",
        "distance": {"text": "50 m", "value": 50},
        "duration": {"text": "12.5 segs", "value": 12},
        "steps": [
            {"instruction": "Dirígete hacia el sur por el pasillo principal", "distance": 22, "direction": "⬇️ SUR"},
            {"instruction": "Gira a la derecha hacia la salida", "distance": 18, "direction": "➡️ DERECHA"},
            {"instruction": "Continúa hasta la puerta principal", "distance": 10, "direction": "⬆️ RECTO"},
            {"instruction": "Has llegado a la entrada principal", "distance": 0, "direction": "🎯 DESTINO"}
        ]
    },
    "Auditorio": {
        "start_address": "Universidad Tecnológica de Panamá, Campus",
        "end_address": "Auditorio César A. Quintero",
        "distance": {"text": "44 m", "value": 44},
        "duration": {"text": "11 segs", "value": 11},
        "steps": [
            {"instruction": "Sal hacia el este", "distance": 16, "direction": "➡️ ESTE"},
            {"instruction": "Gira a la izquierda hacia el área de eventos", "distance": 18, "direction": "⬅️ IZQUIERDA"},
            {"instruction": "El auditorio está a tu derecha", "distance": 10, "direction": "➡️ DERECHA"},
            {"instruction": "Has llegado al auditorio", "distance": 0, "direction": "🎯 DESTINO"}
        ]
    },
    "Laboratorio": {
        "start_address": "Universidad Tecnológica de Panamá, Campus",
        "end_address": "Laboratorios de Ingeniería, Edificio 2",
        "distance": {"text": "40 m", "value": 40},
        "duration": {"text": "10 segs", "value": 10},
        "steps": [
            {"instruction": "Dirígete hacia el edificio de ingeniería", "distance": 18, "direction": "⬆️ RECTO"},
            {"instruction": "Sube al segundo piso", "distance": 10, "direction": "⬆️ ARRIBA"},
            {"instruction": "Gira a la derecha hacia los laboratorios", "distance": 12, "direction": "➡️ DERECHA"},
            {"instruction": "Has llegado al laboratorio", "distance": 0, "direction": "🎯 DESTINO"}
        ]
    }
}

# ==================== FUNCIONES DE SONIDO ====================
def play_beeps(num_beeps):
    """Emite N pitidos según la distancia del objeto"""
    duty = int(32768 * VOLUME)
    
    for i in range(num_beeps):
        if muted:
            SPEAKER_LEFT.duty_u16(0)
            SPEAKER_RIGHT.duty_u16(0)
            return
        
        SPEAKER_LEFT.freq(1200)
        SPEAKER_RIGHT.freq(1200)
        SPEAKER_LEFT.duty_u16(duty)
        SPEAKER_RIGHT.duty_u16(duty)
        time.sleep(0.15)
        
        SPEAKER_LEFT.duty_u16(0)
        SPEAKER_RIGHT.duty_u16(0)
        time.sleep(0.1)

def distance_to_beeps(distance):
    """Convierte distancia a número de pitidos"""
    if distance <= 1.0:
        return 3  # MUY CERCA
    elif distance <= 5.0:
        return 2  # CERCA
    elif distance <= 10.0:
        return 1  # LEJOS
    else:
        return 0  # MUY LEJOS

def speak_word(word):
    """Sintetiza una palabra usando patrones de frecuencia"""
    word_patterns = {
        'navegando': [600, 800, 700, 900],
        'hacia': [500, 700, 600],
        'sal': [700, 900],
        'gira': [800, 600, 900],
        'derecha': [600, 800, 700],
        'izquierda': [900, 700, 600, 800],
        'continua': [700, 900, 800, 700],
        'recto': [800, 600],
        'llegado': [800, 600, 900, 700],
        'destino': [700, 900, 800],
        'sube': [600, 800, 900],
        'edificio': [700, 900, 800, 600],
        'cancelada': [800, 600, 700, 500],
        'del': [500, 700],
        'este': [800, 600],
        'oeste': [600, 800],
        'norte': [700, 900],
        'sur': [900, 700],
        'has': [700, 800],
        'tu': [600, 700],
        'la': [500, 600],
        'hasta': [700, 900, 800]
    }
    
    word_lower = word.lower().strip()
    
    if word_lower in word_patterns:
        freqs = word_patterns[word_lower]
    else:
        freqs = [700, 900, 800]
    
    duty = int(32768 * VOLUME)
    for freq in freqs:
        if muted:
            SPEAKER_LEFT.duty_u16(0)
            SPEAKER_RIGHT.duty_u16(0)
            return
        
        SPEAKER_LEFT.freq(freq)
        SPEAKER_RIGHT.freq(freq)
        SPEAKER_LEFT.duty_u16(duty)
        SPEAKER_RIGHT.duty_u16(duty)
        time.sleep(0.08)
        SPEAKER_LEFT.duty_u16(0)
        SPEAKER_RIGHT.duty_u16(0)
        time.sleep(0.02)

def text_to_speech(text):
    """Convierte texto a voz palabra por palabra"""
    if not muted and text:
        print(f"🔊 {text}")
        
        words = text.split()
        for word in words:
            if muted:
                break
            clean_word = word.strip('.,!?')
            if clean_word:
                speak_word(clean_word)
                time.sleep(0.05)

# ==================== CLASE CAMERA DETECTOR ====================
class CAM_Detector:
    def __init__(self):
        self.frame_width = 640
        self.frame_height = 480
        
    def simulate_yolo_detection(self):
        if random.random() < 0.3:
            detections = []
            for _ in range(random.randint(1, 2)):
                obj_class = random.choice(YOLO_CLASSES)
                confidence = random.uniform(0.50, 0.95)
                x1 = random.randint(0, self.frame_width - 200)
                y1 = random.randint(0, self.frame_height - 200)
                w = random.randint(100, 300)
                h = random.randint(100, 300)
                
                detections.append({
                    'class': obj_class,
                    'confidence': confidence,
                    'bbox': {'x1': x1, 'y1': y1, 'x2': x1 + w, 'y2': y1 + h, 'width': w, 'height': h}
                })
            return detections
        return []
    
    def calculate_distance(self, bbox):
        area = bbox['width'] * bbox['height']
        max_area = self.frame_width * self.frame_height
        normalized_area = area / max_area
        distance = 5.0 - (normalized_area * 4.7)
        return round(distance, 2)
    
    def determine_position(self, bbox):
        center_x = (bbox['x1'] + bbox['x2']) / 2
        if center_x < self.frame_width / 3:
            return "izquierda"
        elif center_x > 2 * self.frame_width / 3:
            return "derecha"
        else:
            return "frente"
    
    def process_detections(self, detections):
        processed = []
        for det in detections:
            if det['confidence'] >= CONFIDENCE_THRESHOLD:
                distance = self.calculate_distance(det['bbox'])
                position = self.determine_position(det['bbox'])
                processed.append({
                    'object': det['class'],
                    'distance': distance,
                    'position': position,
                    'confidence': det['confidence']
                })
        return processed

# ==================== CLASE SENSOR ULTRASÓNICO ====================
class Ultrasonic_Sensor:
    def __init__(self, trig_pin, echo_pin, name):
        self.trig = trig_pin
        self.echo = echo_pin
        self.name = name
        
    def measure_distance(self):
        self.trig.low()
        time.sleep_us(2)
        self.trig.high()
        time.sleep_us(10)
        self.trig.low()
        distance = random.uniform(0.5, 12.0)
        return round(distance, 2)

class Sensors_Detector:
    def __init__(self):
        self.sensor_baston = Ultrasonic_Sensor(TRIG_BASTON, ECHO_BASTON, "baston")
        self.sensor_frente = Ultrasonic_Sensor(TRIG_FRENTE, ECHO_FRENTE, "frente")
        self.last_alert_time = 0
        
    def scan(self):
        dist_baston = self.sensor_baston.measure_distance()
        dist_frente = self.sensor_frente.measure_distance()
        
        closest_distance = min(dist_baston, dist_frente)
        closest_sensor = "baston" if dist_baston < dist_frente else "frente"
        
        num_beeps = distance_to_beeps(closest_distance)
        
        if num_beeps > 0:
            current_time = time.time()
            if current_time - self.last_alert_time >= 1.0:
                print(f"[ULTRASONIC] {closest_sensor.upper()}: {closest_distance}m → {num_beeps} pitido(s)")
                play_beeps(num_beeps)
                self.last_alert_time = current_time
        
        return dist_baston, dist_frente

# ==================== CLASE GOOGLE MAPS NAVIGATOR (SIMULADO) ====================
class GoogleMapsNavigator:
    def __init__(self):
        self.route_steps = []
        self.current_step_index = 0
        self.total_route_distance = 0
        self.current_step_distance = 0
        self.destination_name = ""
        
    def simulate_voice_recognition(self):
        """Lee potenciómetro de voz para seleccionar destino"""
        voice_raw = POT_VOICE.read_u16()
        destinations = list(SIMULATED_ROUTES.keys())
        destination_index = int((voice_raw / 65535) * len(destinations))
        if destination_index >= len(destinations):
            destination_index = len(destinations) - 1
        
        destination_name = destinations[destination_index]
        print(f"[VOZ] Potenciómetro: {voice_raw} → Destino: {destination_name}")
        return destination_name
    
    def get_directions(self, destination_name):
        """Obtiene ruta simulada desde la base de datos offline"""
        global distance_to_destination
        
        if destination_name not in SIMULATED_ROUTES:
            print(f"❌ Destino '{destination_name}' no encontrado")
            return None
        
        route_data = SIMULATED_ROUTES[destination_name]
        self.destination_name = destination_name
        
        print(f"\n📍 RUTA GOOGLE MAPS (Simulada):")
        print(f"   Desde: {route_data['start_address']}")
        print(f"   Hasta: {route_data['end_address']}")
        print(f"   Distancia: {route_data['distance']['text']}")
        print(f"   Duración: {route_data['duration']['text']}\n")
        
        steps = []
        for i, step in enumerate(route_data['steps']):
            steps.append({
                'instruction': step['instruction'],
                'distance': step['distance'],
                'direction': step.get('direction', '')
            })
            if step['distance'] > 0:
                direction_indicator = step.get('direction', '')
                print(f"   {i+1}. {direction_indicator} {step['instruction']} ({step['distance']}m)")
            else:
                print(f"   {i+1}. {step.get('direction', '🎯')} {step['instruction']}")
        
        self.route_steps = steps
        self.current_step_index = 0
        self.total_route_distance = route_data['distance']['value']
        self.current_step_distance = 0
        distance_to_destination = self.total_route_distance
        
        return steps
    
    def update_position(self, time_elapsed):
        """Actualiza posición según velocidad de caminata"""
        global distance_to_destination
        distance_walked = walking_speed * time_elapsed
        self.current_step_distance += distance_walked
        distance_to_destination = max(0, distance_to_destination - distance_walked)
        return distance_walked
    
    def get_current_instruction(self):
        """Obtiene instrucción actual"""
        if self.current_step_index < len(self.route_steps):
            step = self.route_steps[self.current_step_index].copy()
            remaining_in_step = step['distance'] - self.current_step_distance
            
            if remaining_in_step > 0:
                step['remaining_distance'] = remaining_in_step
                return step
            else:
                self.current_step_index += 1
                self.current_step_distance = 0
                return self.get_current_instruction()
        
        return None

# ==================== INSTANCIAS ====================
cam_detector = CAM_Detector()
sensor_detector = Sensors_Detector()
navigator = GoogleMapsNavigator()

# ==================== LOOP PRINCIPAL ====================
def main():
    global system_on, muted, navigation_active, current_step_index
    global last_camera_check, last_ultrasonic_check, last_navigation_update, last_audio_announcement
    global last_detections
    
    print("\n" + "="*60)
    print("ASISTENTE VISUAL INTELIGENTE")
    print("Con Simulador de Google Maps API")
    print("="*60)
    print("\n[CONTROLES]")
    print("BTN_POWER (GP15) - Encender/Apagar")
    print("BTN_MUTE (GP14) - Silenciar Audio")
    print("BTN_NAVIGATION (GP13) - Iniciar GPS")
    print("POTENCIOMETRO (GP27) - Seleccionar Destino")
    print("\n[DESTINOS DISPONIBLES]")
    for i, dest in enumerate(SIMULATED_ROUTES.keys()):
        print(f"  {i+1}. {dest}")
    print("\n[PITIDOS ULTRASONIDO]")
    print("1 pitido  = 5-10m")
    print("2 pitidos = 1-5m")
    print("3 pitidos = <1m\n")
    
    last_power_state = 1
    last_mute_state = 1
    last_nav_state = 1
    
    while True:
        current_time = time.time()
        
        # Botón POWER
        power_state = BTN_POWER.value()
        if power_state == 0 and last_power_state == 1:
            system_on = not system_on
            LED_STATUS.value(system_on)
            print(f"\n{'✓ SISTEMA ENCENDIDO' if system_on else '✗ SISTEMA APAGADO'}")
            if not system_on:
                LED_NAVIGATION.off()
                LED_DETECTION.off()
                navigation_active = False
                SPEAKER_LEFT.duty_u16(0)
                SPEAKER_RIGHT.duty_u16(0)
        last_power_state = power_state
        
        # Botón MUTE
        mute_state = BTN_MUTE.value()
        if mute_state == 0 and last_mute_state == 1:
            muted = not muted
            print(f"{'🔇 Audio silenciado' if muted else '🔊 Audio activado'}")
        last_mute_state = mute_state
        
        # Botón NAVIGATION
        nav_state = BTN_NAVIGATION.value()
        if nav_state == 0 and last_nav_state == 1 and system_on:
            if not navigation_active:
                destination_name = navigator.simulate_voice_recognition()
                navigator.get_directions(destination_name)
                navigation_active = True
                current_step_index = 0
                last_navigation_update = current_time
                last_audio_announcement = current_time
                LED_NAVIGATION.on()
                text_to_speech(f"navegando hacia {destination_name}")
            else:
                navigation_active = False
                current_step_index = 0
                LED_NAVIGATION.off()
                print("🛑 Navegación cancelada")
                text_to_speech("navegando cancelada")
        last_nav_state = nav_state
        
        # SISTEMA ACTIVO
        if system_on:
            
            # CÁMARA (cada 1 segundo)
            if current_time - last_camera_check >= CAMERA_INTERVAL:
                LED_DETECTION.on()
                raw_detections = cam_detector.simulate_yolo_detection()
                processed_detections = cam_detector.process_detections(raw_detections)
                
                if processed_detections:
                    print(f"[CAM] Detectados {len(processed_detections)} objetos")
                    for det in processed_detections[:1]:
                        obj_name = det['object'].replace('_', ' ')
                        print(f"  → {obj_name} a {det['distance']}m ({det['position']})")
                    last_detections = processed_detections
                
                LED_DETECTION.off()
                last_camera_check = current_time
            
            # ULTRASONIDOS (cada 3 segundos)
            if current_time - last_ultrasonic_check >= ULTRASONIC_INTERVAL:
                sensor_detector.scan()
                last_ultrasonic_check = current_time
            
            # NAVEGACIÓN GPS (cada 1 segundo)
            if navigation_active and current_time - last_navigation_update >= NAVIGATION_INTERVAL:
                time_elapsed = current_time - last_navigation_update
                navigator.update_position(time_elapsed)
                
                instruction = navigator.get_current_instruction()
                
                if instruction:
                    remaining = instruction.get('remaining_distance', instruction['distance'])
                    direction = instruction.get('direction', '')
                    print(f"[GPS] {direction} | Distancia restante: {distance_to_destination:.0f}m")
                    
                    if current_time - last_audio_announcement >= AUDIO_INTERVAL:
                        text_to_speech(instruction['instruction'])
                        last_audio_announcement = current_time
                else:
                    print("[GPS] 🎯 ¡Destino alcanzado!")
                    text_to_speech("has llegado a tu destino")
                    navigation_active = False
                    current_step_index = 0
                    LED_NAVIGATION.off()
                
                last_navigation_update = current_time
        
        time.sleep(0.05)

# ==================== EJECUCIÓN ====================
try:
    main()
except KeyboardInterrupt:
    print("\n\n[SISTEMA] Apagado manual")
    SPEAKER_LEFT.duty_u16(0)
    SPEAKER_RIGHT.duty_u16(0)
    LED_STATUS.off()
    LED_NAVIGATION.off()
    LED_DETECTION.off()