import socket
import time

try:
    import network  # type: ignore[import-not-found]
    from machine import UART, Pin  # type: ignore[import-not-found]
except ImportError:
    class Pin:
        def __init__(self, *args, **kwargs):
            pass

    class UART:
        def __init__(self, *args, **kwargs):
            pass

        def write(self, *args, **kwargs):
            pass

    class _DummyWLAN:
        AP_IF = "AP_IF"

        def __init__(self, *args, **kwargs):
            self._active = False

        def config(self, **kwargs):
            pass

        def active(self, value=None):
            if value is not None:
                self._active = bool(value)
            return self._active

        def ifconfig(self):
            return ("192.168.4.1", "255.255.255.0", "192.168.4.1", "8.8.8.8")

    class network:
        AP_IF = "AP_IF"
        WLAN = _DummyWLAN

# UART para comunicarse con la Tang Nano
uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)


# Wi-Fi creado por el Pico W
wifi = network.WLAN(network.AP_IF)

wifi.config(
    essid="Robot",
    password="robot1234"
)

wifi.active(True)

while not wifi.active():
    time.sleep(0.1)


# Pagina web del control
html = """
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Robot</title>

<style>

body {
    background-color: #111;
    color: white;
    font-family: Arial;
    text-align: center;
}

h1 {
    margin-top: 20px;
}

button {
    width: 90px;
    height: 70px;
    margin: 7px;
    font-size: 25px;
    font-weight: bold;
    border: none;
    border-radius: 12px;
}

.control {
    background-color: white;
    color: black;
}

.stop {
    background-color: red;
    color: white;
}

button:active {
    transform: scale(0.95);
}

</style>

</head>


<body>

<h1>ROBOT</h1>

<p>Control del robot</p>


<div>

<button class="control"
onclick="sendCommand('F')">
▲
</button>

</div>


<div>

<button class="control"
onclick="sendCommand('L')">
◀
</button>


<button class="stop"
onclick="sendCommand('S')">
STOP
</button>


<button class="control"
onclick="sendCommand('R')">
▶
</button>

</div>


<div>

<button class="control"
onclick="sendCommand('B')">
▼
</button>

</div>


<p id="estado">
Robot detenido
</p>


<script>

function sendCommand(command) {

    fetch("/cmd?val=" + command)

    .then(response => response.text())

    .then(data => {

        document.getElementById("estado").innerText =
        "Comando: " + command;

    })

    .catch(error => {

        document.getElementById("estado").innerText =
        "Error";

    });

}

</script>

</body>

</html>
"""


# Servidor web
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("", 80))

server.listen(1)


# Esperar conexiones del celular
while True:

    conn, addr = server.accept()

    request = conn.recv(1024)

    request = str(request)


    # Recibir comando
    if "/cmd?val=" in request:

        command = request.split(
            "/cmd?val="
        )[1].split(" ")[0]


        # Comandos permitidos
        if command in ["F", "B", "L", "R", "S"]:

            uart.write(command.encode())

            response = "OK"

        else:

            response = "Comando no valido"


        # Respuesta al celular
        conn.send(
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            + response
        )


    # Mostrar pagina web
    else:

        conn.send(
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            + html
        )


    conn.close()