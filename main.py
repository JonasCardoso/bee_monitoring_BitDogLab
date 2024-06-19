import network
import ufirebase as firebase
import time
import utime

from _thread import start_new_thread
from sensors_manager import SensorsManager

REDE = "Jonathan's"
SENHA = "johnny123"

### Conexão wi-fi, com rede e senha pré-definidos
GLOB_WLAN = network.WLAN(network.STA_IF)
GLOB_WLAN.active(True)

counter = 0
print("Tentativas de conexão à rede wi-fi", REDE, ":", end='')
while not GLOB_WLAN.isconnected():
    GLOB_WLAN.connect(REDE, SENHA)
    counter += 1
    print(counter, ", ", end='')
    time.sleep(4)
    pass
print("Wi-fi Conectado")

### Definição do URL do firebase
firebase.setURL("https://bee-rasp-default-rtdb.firebaseio.com/")

### Instanciação das Classes Gerenciadoras
sensors_manager = SensorsManager()
start_new_thread(sensors_manager.sensors_reading, ())