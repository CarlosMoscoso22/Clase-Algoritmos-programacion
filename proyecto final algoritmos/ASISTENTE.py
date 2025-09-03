import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

# Inicializar motor de voz
engine = pyttsx3.init()

def hablar(texto):
    """Convierte texto en voz"""
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    """Escucha por micrófono y convierte voz en texto"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Reconociendo...")
        comando = r.recognize_google(audio, language="es-ES")
        print(f"Tú dijiste: {comando}\n")
    except Exception:
        print("No entendí, repite por favor...")
        return "None"
    return comando.lower()

def asistente():
    hablar("Hola, soy tu asistente. ¿Qué deseas?")
    while True:
        comando = escuchar()

        if "hora" in comando:
            hora = datetime.datetime.now().strftime("%H:%M")
            hablar(f"Son las {hora}")

        elif "buscar" in comando:
            hablar("¿Qué quieres que busque en Google?")
            busqueda = escuchar()
            url = f"https://www.google.com/search?q={busqueda}"
            webbrowser.open(url)
            hablar(f"Buscando {busqueda} en Google")

        elif "chiste" in comando:
            chistes = [
                "¿Por qué la computadora fue al médico? Porque tenía un virus.",
                "¿Qué le dice un bit al otro? Nos vemos en el bus.",
                "¿Cuál es el animal más antiguo? La cebra, porque está en blanco y negro."
            ]
            hablar(random.choice(chistes))

        elif "salir" in comando or "adiós" in comando:
            hablar("Adiós, fue un placer ayudarte.")
            break

        elif comando != "None":
            hablar("Lo siento, no tengo esa función aún.")

# Ejecutar asistente
asistente()