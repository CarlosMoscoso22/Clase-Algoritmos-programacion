import speech_recognition as sr 
import pyttsx3
import datetime
import webbrowser
import random
engine= pyttsx3.init()
def hablar(texto):#convierte el texto en voz
    engine.say(texto)
    engine.runAndWait()
def escuchar(): # escucha por microfono y convierte el texto en voz
    r= sr.Recognizer()
    with sr.Microphone as source
    print("escuchando")
    r.pause_threshold=1