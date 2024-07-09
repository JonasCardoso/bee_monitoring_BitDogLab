from connections_manager import connect_to_wifi
from sensors_manager import SensorsManager

connect_to_wifi()

### Instanciação das Classes Gerenciadoras
sensors_manager = SensorsManager()
sensors_manager.sensors_reading()