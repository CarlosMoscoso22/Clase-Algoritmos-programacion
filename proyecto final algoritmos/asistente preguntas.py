import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
from bs4 import BeautifulSoup

# Inicializar motor de voz
engine = pyttsx3.init()

def configurar_voz():
    voices = engine.getProperty("voices")
    for v in voices:
        if "spanish" in v.id.lower():
            engine.setProperty("voice", v.id)
            break
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1)

def hablar(texto):
    print("🤖 Asistente:", texto)
    engine.say(texto)
    engine.runAndWait()

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

def buscar_google(pregunta):
    url = f"https://www.google.com/search?q={pregunta}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    respuesta = soup.find("div", class_="BNeawe")
    if respuesta:
        return respuesta.text
    else:
        return "No encontré una respuesta clara en Google."

def buscar_wikipedia(pregunta):
    try:
        wikipedia.set_lang("es")
        resumen = wikipedia.summary(pregunta, sentences=2)
        return resumen
    except:
        return "No encontré información en Wikipedia."

def asistente():
    configurar_voz()
    hablar("Hola Felipe, soy tu asistente. Pregúntame lo que quieras.")
    while True:
        comando = escuchar()
        if comando == "":
            continue
        if "salir" in comando:
            hablar("Adiós, hasta pronto.")
            break
        elif "wikipedia" in comando:
            tema = comando.replace("wikipedia", "")
            respuesta = buscar_wikipedia(tema)
            hablar(respuesta)
        else:
            # primero prueba Wikipedia
            respuesta = buscar_wikipedia(comando)
            if "No encontré" in respuesta:
                respuesta = buscar_google(comando)
            hablar(respuesta)

if __name__ == "__main__":
    asistente()