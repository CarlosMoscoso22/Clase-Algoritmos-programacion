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


# UART para la comunicación con la Tang Nano
uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)


# Crear punto de acceso Wi‑Fi
wifi = network.WLAN(network.AP_IF)
wifi.config(essid="Robot", password="robot1234")
wifi.active(True)

while not wifi.active():
    time.sleep(0.1)

print("Robot iniciado")
print("WiFi: Robot")
print("IP:", wifi.ifconfig()[0])


html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Control</title>
    <style>
        :root {
            --bg: #0d1117;
            --panel: #151b22;
            --panel-2: #1d2732;
            --text: #edf2f7;
            --muted: #a9b6c3;
            --accent: #7dd3fc;
            --accent-2: #38bdf8;
            --danger: #ef4444;
            --button: #f5f7fa;
            --shadow: rgba(0, 0, 0, 0.35);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at top, #1f2a38 0%, var(--bg) 45%);
            color: var(--text);
            font-family: Arial, Helvetica, sans-serif;
            text-align: center;
        }

        .panel {
            width: min(92vw, 420px);
            background: rgba(21, 27, 34, 0.94);
            border: 1px solid rgba(125, 211, 252, 0.25);
            border-radius: 22px;
            box-shadow: 0 18px 50px var(--shadow);
            padding: 22px 20px 18px;
        }

        h1 {
            margin: 8px 0 6px;
            font-size: clamp(2rem, 5vw, 2.6rem);
            letter-spacing: 1px;
        }

        .subtitle {
            margin: 0 0 18px;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .pad {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .row {
            display: flex;
            justify-content: center;
            gap: 12px;
        }

        button {
            width: 92px;
            height: 70px;
            border: none;
            border-radius: 16px;
            font-size: 2rem;
            font-weight: 700;
            cursor: pointer;
            background: linear-gradient(180deg, #f8fafc 0%, #dfe6ee 100%);
            color: #101827;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
            transition: transform 0.08s ease, box-shadow 0.15s ease;
            user-select: none;
        }

        button:active {
            transform: translateY(2px) scale(0.97);
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.18);
        }

        .stop {
            background: linear-gradient(180deg, #f87171 0%, #dc2626 100%);
            color: white;
            width: 110px;
            font-size: 1.2rem;
        }

        .status {
            margin-top: 18px;
            padding: 12px 14px;
            border-radius: 12px;
            background: var(--panel-2);
            border: 1px solid rgba(255, 255, 255, 0.06);
            color: var(--text);
            font-weight: 700;
            min-height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    <div class="panel">
        <h1>ROBOT</h1>
        <p class="subtitle">Control del robot</p>

        <div class="pad">
            <div class="row">
                <button onclick="sendCommand('F')">▲</button>
            </div>

            <div class="row">
                <button onclick="sendCommand('L')">◀</button>
                <button class="stop" onclick="sendCommand('S')">STOP</button>
                <button onclick="sendCommand('R')">▶</button>
            </div>

            <div class="row">
                <button onclick="sendCommand('B')">▼</button>
            </div>
        </div>

        <div id="estado" class="status">Robot detenido</div>
    </div>

    <script>
        function setStatus(text) {
            document.getElementById('estado').innerText = text;
        }

        function sendCommand(command) {
            setStatus('Enviando ' + command + '...');

            fetch('/cmd?val=' + command)
                .then(function(response) {
                    return response.text();
                })
                .then(function() {
                    setStatus('Comando: ' + command);
                })
                .catch(function() {
                    setStatus('Error de comunicación');
                });
        }
    </script>
</body>
</html>
"""


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 80))
server.listen(1)

print("Servidor web iniciado")
print("Conecta desde tu celular a:")
print("http://192.168.4.1")

while True:
    conn, addr = server.accept()
    print("Cliente conectado:", addr)

    try:
        request = conn.recv(1024)
        request = str(request)

        if "/cmd?val=" in request:
            command = request.split("/cmd?val=")[1].split(" ")[0]

            if command in ["F", "B", "L", "R", "S"]:
                uart.write(command.encode())
                response = "OK"
            else:
                response = "Comando no valido"

            conn.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                + response
            )
        else:
            conn.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "\r\n"
                + html
            )
    except Exception as e:
        print("Error HTTP:", e)
    finally:
        conn.close()