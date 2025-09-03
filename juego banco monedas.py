#juego banco monedas de color rojo o azul
import json
from datetime import datetime

# Tesoro inicial
tesoro = {"rojo": 120, "azul": 85}
eventos = [] # lista de movimientos

# Guardar en JSON
def guardar():
    with open("tesoro.json", "w") as f:
        json.dump({"tesoro": tesoro, "eventos": eventos}, f, indent=4)
    print(" Tesoro guardado.")

# Cargar desde JSON
def cargar():
    global tesoro, eventos
    try:
        with open("tesoro.json", "r") as f:
            data = json.load(f)
            tesoro = data["tesoro"]
            eventos = data["eventos"]
        print(" Tesoro cargado.")
    except FileNotFoundError:
        print(" No hay archivo guardado todavía.")

# Depositar
def depositar(color, monto):
    if monto > 0:
        tesoro[color] = tesoro.get(color, 0) + monto
        registrar_evento("depositar", color, monto)
        print(f"Depositaste {monto} en {color}.")
    else:
        print(" El monto debe ser positivo.")

# Retirar
def retirar(color, monto):
    i
