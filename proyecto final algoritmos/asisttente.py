import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty("rate", 170) # Velocidad de la voz
engine.setProperty("volume", 1) # Volumen al máximo

def hablar(texto):
    print("Asistente:", texto)
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="es-ES")
        print(f"🙋 Tú dijiste: {query}")
    except sr.UnknownValueError:
        hablar("No entendí, repite por favor.")
        return ""
    return query.lower()

def ejecutar_comando(query):
    if "hora" in query:
        hora = datetime.datetime.now().strftime("%H:%M")
        hablar(f"La hora actual es {hora}")

    elif "chiste" in query:
        chiste = pyjokes.get_joke(language="es", category="all")
        hablar(chiste)

    elif "busca" in query:
        tema = query.replace("busca", "").strip()
        if tema:
            try:
                resultado = wikipedia.summary(tema, sentences=2, auto_suggest=True, redirect=True)
                hablar(f"Según Wikipedia: {resultado}")
            except:
                hablar("No encontré información en Wikipedia, pero te lo muestro en Google.")
                webbrowser.open(f"https://www.google.com/search?q={tema}")
        else:
            hablar("¿Qué quieres que busque?")

    elif "abre google" in query:
        hablar("Abriendo Google.")
        webbrowser.open("https://www.google.com")

    elif "adiós" in query or "salir" in query:
        hablar("Hasta luego, Felipe. Fue un placer ayudarte.")
        exit()

    else:
        hablar("No entendí tu orden, intenta de nuevo.")

# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    hablar("Hola Felipe, soy tu asistente virtual. Pregúntame lo que quieras.")
    while True:
        consulta = escuchar()
        if consulta != "":
            ejecutar_comando(consulta)