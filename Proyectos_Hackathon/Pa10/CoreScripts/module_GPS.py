import time
import json
import signal
import pyttsx3
import threading
import queue


RUNNING = True

class NavigationAudioNotifier:
    """TTS robusto para navegación GPS (offline)"""

    def __init__(self, rate=150, volume=0.9, language="es"):
        self.rate = rate
        self.volume = volume
        self.language = language

        self.audio_queue = queue.Queue()
        self.is_speaking = False
        self.is_running = True

        self.audio_thread = threading.Thread(
            target=self._process_audio_queue,
            daemon=True
        )
        self.audio_thread.start()

    # =============================
    # MÉTODO PÚBLICO
    # =============================
    def speak(self, text: str, blocking=False):
        self.audio_queue.put({"text": text})

        if blocking:
            while not self.audio_queue.empty() or self.is_speaking:
                time.sleep(0.1)

    # =============================
    # THREAD DE AUDIO (CLAVE)
    # =============================
    def _process_audio_queue(self):
        while self.is_running:
            try:
                task = self.audio_queue.get(timeout=1)
                self.is_speaking = True

                engine = pyttsx3.init()
                engine.setProperty("rate", self.rate)
                engine.setProperty("volume", self.volume)

                for voice in engine.getProperty("voices"):
                    if "spanish" in voice.name.lower() or "es" in voice.id.lower():
                        engine.setProperty("voice", voice.id)
                        break

                engine.say(task["text"])
                engine.runAndWait()

                del engine
                self.is_speaking = False
                self.audio_queue.task_done()

            except queue.Empty:
                self.is_speaking = False
            except Exception as e:
                print(f"[TTS ERROR] {e}")
                self.is_speaking = False

    # =============================
    # NAVEGACIÓN
    # =============================
    def announce_route(self, distance, duration):
        self.speak(
            f"Ruta calculada. Distancia total {distance}. "
            f"Duración estimada {duration}"
        )

    def announce_step(self, instruction, distance):
        self.speak(
            f"{instruction}. Continúe por {distance}"
        )

    def wait_until_done(self):
        self.audio_queue.join()

    def shutdown(self):
        self.is_running = False
        self.audio_thread.join(timeout=2)

def stop_program(signal_received, frame):
    global RUNNING
    print("\n🛑 Señal de detención recibida. Cerrando sistema...")
    RUNNING = False


signal.signal(signal.SIGINT, stop_program)


def load_route_from_mock(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    global RUNNING

    notifier = NavigationAudioNotifier(rate=120)

    data = load_route_from_mock(r"C:\Users\TheBe\OneDrive\Escritorio\U\Hackaton\ruta_prueba.json")
    direction = data["directions"][0]

    print("🚀 Sistema de navegación iniciado")

    try:
        while RUNNING:
            # Resumen solo UNA vez (o cuando quieras)
            notifier.announce_route(
                direction["formatted_distance"],
                direction["formatted_duration"]
            )

            # Leer pasos
            for trip in direction["trips"]:
                for step in trip["details"]:
                    if not RUNNING:
                        break

                    notifier.announce_step(
                        step["title"],
                        step["formatted_distance"]
                    )
                    time.sleep(1)

            # Evita que vuelva a repetir la ruta infinitamente
            print("🧭 Ruta finalizada. Esperando Ctrl+C...")
            while RUNNING:
                time.sleep(0.5)

    finally:
        print("🔇 Apagando TTS...")
        notifier.shutdown()
        print("✅ Sistema detenido correctamente")


if __name__ == "__main__":
    main()

