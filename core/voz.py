import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import tempfile
import os

def escuchar_y_transcribir(callback_exito, callback_error):
    """
    Graba 5 segundos de audio del micrófono y lo transcribe usando Google.
    Llama a callback_exito(texto) o callback_error(mensaje).
    """
    temp_path = None
    try:
        fs = 44100  # Frecuencia de muestreo
        duration = 5  # Segundos de grabación
        
        # Iniciar grabación (el hilo se bloquea aquí por 5 segundos)
        grabacion = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        
        # Guardar archivo temporal
        fd, temp_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        sf.write(temp_path, grabacion, fs)
        
        # Reconocimiento
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
            texto = recognizer.recognize_google(audio, language='es-ES')
            
        callback_exito(texto)
        
    except sr.UnknownValueError:
        callback_error("No se entendió el audio.")
    except sr.RequestError as e:
        callback_error(f"Error de conexión: {e}")
    except Exception as e:
        callback_error(f"Error al grabar: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
