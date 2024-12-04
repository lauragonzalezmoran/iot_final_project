import pygame
import time

# Inicializa el módulo de mixer de pygame
pygame.mixer.init()

# Función para reproducir una alarma
def alarma(archivo_mp3):
    """Reproduce un archivo MP3."""
    try:
        pygame.mixer.music.load(archivo_mp3)  # Carga el archivo MP3
        pygame.mixer.music.play(-1)  # Reproduce en bucle infinito
        print("Alarma sonando...")
    except Exception as e:
        print(f"Error al reproducir la alarma: {e}")

# Función para detener la alarma
def stop_alarma():
    """Detiene la reproducción de la alarma."""
    try:
        pygame.mixer.music.stop()  # Detiene la música
        print("Alarma detenida.")
    except Exception as e:
        print(f"Error al detener la alarma: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    archivo_mp3 = "alarm.mp3"  # Cambia esto por la ruta de tu archivo MP3
    alarma(archivo_mp3)
    time.sleep(10)  # Deja que la alarma suene por 10 segundos
    stop_alarma()
