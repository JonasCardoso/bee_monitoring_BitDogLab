import network
import ufirebase as firebase
import time
import utime

from _thread import start_new_thread
from sensors_manager import SensorsManager

### Conexão wi-fi, com rede e senha pré-definidos
print("Tentando conectar à rede wi-fi Jonathan's:")
GLOB_WLAN = network.WLAN(network.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("Jonathan's", "johnny123")

counter = 0
while not GLOB_WLAN.isconnected():
    counter += 1
    print("Não Conectado ", counter)
    time.sleep(1)
    pass
print("Wi-fi Conectado")

### Definição do URL do firebase
firebase.setURL("https://bee-rasp-default-rtdb.firebaseio.com/")

### Instanciação das Classes Gerenciadoras
sensors_manager = SensorsManager()
start_new_thread(sensors_manager.sensors_reading, ())
