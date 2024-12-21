import pygame
import time

# Initialize the pygame mixer module for audio playback.
pygame.mixer.init()

# Function to play an alarm sound.
def alarma(archivo_mp3):
    """
    Play an alarm sound using the specified MP3 file.

    This function uses the pygame mixer module to load and play
    an alarm sound in an infinite loop until explicitly stopped.

    Parameters:
    archivo_mp3 (str): Path to the MP3 file to be played.

    Raises:
    Exception: If there is an error loading or playing the MP3 file.

    Example:
    alarma("alarm.wav")
    """
    try:
        pygame.mixer.music.load(archivo_mp3)  # Load the specified MP3 file.
        pygame.mixer.music.play(-1)  # Play the sound on an infinite loop.
        print("Alarm is sounding...")  # Log that the alarm is sounding.
    except Exception as e:
        print(f"Error playing the alarm: {e}")  # Log any errors encountered.

# Function to stop the alarm sound.
def stop_alarma():
    """
    Stop the currently playing alarm sound.

    This function stops the playback of the alarm sound
    that was started using the `alarma` function.

    Raises:
    Exception: If there is an error stopping the MP3 playback.

    Example:
    stop_alarma()
    """
    try:
        pygame.mixer.music.stop()  # Stop the currently playing music.
        print("Alarm has been stopped.")  # Log that the alarm has stopped.
    except Exception as e:
        print(f"Error stopping the alarm: {e}")  # Log any errors encountered.

# Example usage (commented out to avoid running in module context):
'''
if __name__ == "__main__":
    # Specify the path to the alarm sound file.
    archivo_mp3 = "alarm.wav"  # Replace with your alarm file path.
    
    # Play the alarm sound.
    alarma(archivo_mp3)
    
    # Allow the alarm to sound for 10 seconds.
    time.sleep(10)
    
    # Stop the alarm sound.
    stop_alarma()
'''
