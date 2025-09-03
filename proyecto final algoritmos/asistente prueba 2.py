import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import random

# Inicializar motor de voz
engine = pyttsx3.init()

def hablar(texto):
    print("🤖 Asistente:", texto) # también lo imprime en terminal
    engine.say(texto)
    engine.runAndWait()

# Función para escuchar
def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="es-CO")
        print("👂 Tú dijiste:", texto)
        return texto.lower()
    except:
        hablar("No entendí, repite por favor")
        return ""

# Función principal
def asistente():
    hablar("Hola, soy tu asistente. Dime un comando")

    while True:
        comando = escuchar()

        if comando == "":
            continue # si no entiende, vuelve a escuchar

        # Acciones según comando
        if "hora" in comando:
            hora = datetime.datetime.now().strftime("%I:%M %p")
            hablar(f"Son las {hora}")

        elif "google" in comando:
            hablar("Abriendo Google")
            webbrowser.open("https://www.google.com")

        elif "chiste" in comando:
            chistes = [
                "¿Por qué la computadora fue al médico? Porque tenía un virus.",
                "¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando.",
                "¿Cuál es el animal más antiguo? La cebra, porque está en blanco y negro."
            ]
            hablar(random.choice(chistes))

        elif "salir" in comando or "adiós" in comando:
            hablar("Adiós, fue un gusto ayudarte.")
            break

        else:
            hablar("Escuché: " + comando + ". Pero no tengo un comando para eso.")

# Ejecutar
asistente()