import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyjokes
from gtts import gTTS
import os
import pygame
import uuid
import time

# Configurar Wikipedia en español
wikipedia.set_lang("es")

# Inicializar pygame mixer
pygame.mixer.init()

def hablar(texto, voz="femenina"):
    print("Asistente:", texto)

    # Selección de voz
    lang = "es"
    tld = "com" if voz == "masculina" else "com.mx"

    # Generar archivo único
    archivo = f"voz_{uuid.uuid4().hex}.mp3"

    # Crear audio
    tts = gTTS(text=texto, lang=lang, tld=tld)
    tts.save(archivo)

    # Reproducir con pygame
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play()

    # Esperar hasta que termine
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Descargar el archivo de pygame antes de borrar
    pygame.mixer.music.unload()
    try:
        os.remove(archivo)
    except PermissionError:
        pass # Si Windows no lo suelta aún, simplemente lo dejamos

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        hablar("Estoy escuchando...", voz="femenina")
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

    elif "busca" in query or "qué es" in query:
        tema = query.replace("busca", "").replace("qué es", "").strip()
        if tema:
            try:
                resultado = wikipedia.summary(tema, sentences=2, auto_suggest=True, redirect=True)
                hablar(f"Según Wikipedia: {resultado}")
            except Exception:
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
    hablar("Hola Felipe, soy tu asistente virtual. Pregúntame lo que quieras.", voz="femenina")
    while True:
        consulta = escuchar()
        if consulta != "":
            ejecutar_comando(consulta)
