import time

try:
    import network  # type: ignore[import-not-found]
except ImportError:
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


wifi = network.WLAN(network.AP_IF)

wifi.active(True)

wifi.config(
    essid="Robot",
    password="robot1234"
)

while not wifi.active():
    time.sleep(1)

print("WiFi iniciado")
print("Nombre: Robot")
print("IP:", wifi.ifconfig()[0])