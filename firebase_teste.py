import network
import ufirebase as firebase
import time

GLOB_WLAN = network.WLAN(network.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect("Cardoso 2.4 GHz", "48963215pjn")

while not GLOB_WLAN.isconnected():
    pass

firebase.setURL("https://bee-rasp-default-rtdb.firebaseio.com/")

while 1:
    time.sleep(5)
    gmtime = list(map(str, time.gmtime()))
    dia = ('00' + gmtime[2])[-2:]
    mes = ('00' + gmtime[1])[-2:]
    ano = gmtime[0]
    hora = ('00' + gmtime[3])[-2:]
    minuto = ('00' + gmtime[4])[-2:]
    segundo = ('00' + gmtime[5])[-2:]
    timestamp = f"{dia}_{mes}_{ano}-{hora}_{minuto}_{segundo}"
    print("Timestamp:", timestamp)

    firebase.put("bee_data/" + timestamp, {"temperatura": 1, "umidade": 2}, bg=0)