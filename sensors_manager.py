import uos
import machine
from time import sleep, localtime, time, gmtime
import utime
import openweathermap as weather
from machine import Pin, I2C
from bme680 import *
from _thread import start_new_thread

# print("Machine: \t" + uos.uname() [4])
# print("MicroPython: \t" + uos.uname()[3])
 
# i2c=I2C(0,scl=Pin(21), sda=Pin (20)) 
# bme = BME680_I2C(i2c=i2c)
# uarto=machine.UART(0, baudrate=115200)

# Define the offset for 'America/Sao_Paulo' in seconds
# São Paulo is UTC-3
timezone_offset = -3 * 3600
current_time = utime.time()
adjusted_time = current_time + timezone_offset
utime.localtime(adjusted_time)
local_time = utime.localtime()

class SensorsManager:
    def __init__(self):
        self.bme680_internal, self.bme680_external = self.__try_to_set_bme680()
        
        self.sensors = {
            'proximity': {'object': self.__set_proximity_sensor(), 'read_method': self.__read_proximity},
            #'internal_sound': {'object': self.__set_internal_sound_sensor(), 'read_method': self.__read_internal_sound},
            #'external_sound': {'object': self.__set_external_sound_sensor(), 'read_method': self.__read_external_sound},
            'internal_temperature': {'object': self.bme680_internal, 'read_method': self.__read_temperature},
            'internal_pressure': {'object': self.bme680_internal, 'read_method': self.__read_pressure},
            'internal_humidity': {'object': self.bme680_internal, 'read_method': self.__read_humidity},
            'internal_gas': {'object': self.bme680_internal, 'read_method': self.__read_gas},
            'external_temperature': {'object': self.bme680_external, 'read_method': self.__read_temperature},
            'external_pressure': {'object': self.bme680_external, 'read_method': self.__read_pressure},
            'external_humidity': {'object': self.bme680_external, 'read_method': self.__read_humidity},
            'external_gas': {'object': self.bme680_external, 'read_method': self.__read_gas}
        }
        
        self.timer = 60
        self.proximity_counter = 0
    
    def __read_sensors(self):
        readings = {}

        for sensor_type in self.sensors:
            read_method = self.sensors[sensor_type]['read_method']
            sensor = self.sensors[sensor_type]['object']

            reading = read_method(sensor)
            readings[sensor_type] = reading

        print(readings)
        return readings

# """
#     def __read_sensors(self):
#         readings = {}
#         readings["Temperatura interna"] = self.__read_temperature(self.bme680_internal)
#         readings["Umidade interna"] = self.__read_humidity(self.bme680_internal)
#         readings["Pressão interna"] = self.__read_pressure(self.bme680_internal)
#         readings["Qualidade ar interna"] = self.__read_gas(self.bme680_internal)
#         
#         readings["Temperatura externa"] = self.__read_temperature(self.bme680_external)
#         readings["Umidade externa"] = self.__read_humidity(self.bme680_external)
#         readings["Pressão externa"] = self.__read_pressure(self.bme680_external)
#         readings["Qualidade ar externa"] = self.__read_gas(self.bme680_external)
#         print(readings)
#         return readings
# """
    def sensors_reading(self):
        #print('timer {0}'.format(self.timer))
        while True:
            readings = self.__read_sensors()

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
            weather_data = weather.get_weather_data()
            sensor_data = {"id_placa": 1, "proximidade": 1,
                            "temperatura_interna": 1, "umidade_interna": 2, "pressao_interna": 2, "ar_interno": 2,
                            "temperatura_externa": 1, "umidade_externa": 2, "pressao_externa": 2, "ar_externo": 2}
                            
            dados = {"sensor": sensor_data, "openweathermap": weather_data}
            
            print("READINGS ", readings)
            #firebase.put("bee_data/" + timestamp, dados, bg=0)
            
            #timestamp = time() * 1000
            #readings = self.__read_sensors()
            #return readings
            #self.database_manager.save_readings(timestamp, readings)

### Inicialização microfones
    def __set_internal_sound_sensor(self):
        return machine.ADC(26)

    def __set_external_sound_sensor(self):
        return machine.ADC(27)
    
### Leitura microfones
    def __read_internal_sound(self, sensor):
        return sensor.read_u16()
    
    def __read_external_sound(self, sensor):
        return sensor.read_u16()
    
    
### Inicialização sensor de proximidade
    def __set_proximity_sensor(self):
        return machine.Pin(2, machine.Pin.IN)

### Leitura sensor de proximidade
    def __read_proximity(self, sensor):
        initial_time = time.time()

        while True:
            if time.time() - initial_time >= self.timer:
                #print(self.proximity_counter)
                return self.proximity_counter
            
            if self.__new_day():
                old_proximity_counter = self.proximity_counter
                self.proximity_counter = 0

                return old_proximity_counter

            reading = sensor.value()
            self.proximity_counter += 1 if reading == 0 else 0
            sleep(0.05)
            
    def __new_day(self):
        local_time = localtime()
        return local_time[3] == 0 and local_time[4] < 1 and local_time[5] < 3

### Inicialização dos dois sensores BME680
    def __set_bme680_internal(self):
        internal_i2c = machine.I2C(0, scl=Pin(21), sda=Pin(20))
        internal_bme = BME680_I2C(i2c=internal_i2c)
        return internal_bme
    def __set_bme680_external(self):
        external_i2c = machine.I2C(0, scl=Pin(25), sda=Pin(24))
        external_bme = BME680_I2C(i2c=external_i2c)
        return external_bme

    def __try_to_set_bme680(self):
        bme680_internal = None
        bme680_external = None
        print("Tentando setar os BME680:")
        while bme680_internal is None or bme680_external is None:
            try:
                bme680_internal = self.__set_bme680_internal()
                print("Internal BME680 set successfully")
            except Exception as e:
                print(f'Failed to set internal BME680: {e}')
                bme680_internal = None
            
            try:
                bme680_external = self.__set_bme680_external()
                print("External BME680 set successfully")
            except Exception as e:
                print(f'Failed to set external BME680: {e}')
                bme680_external = None
            
            if bme680_internal is None or bme680_external is None:
                print('bme bad functioning, trying again in 3 seconds')
                time.sleep(3)
                
        return bme680_internal, bme680_external



### Leituras BME680
    def __read_temperature(self, bme):
        if bme is None:
            return None
        else:
            return bme.temperature

    def __read_humidity(self, bme):
        if bme is None:
            return None
        else:
            return bme.humidity

    def __read_pressure(self, bme):
        if bme is None:
            return None
        else:
            return bme.pressure

    def __read_gas(self, bme):
        if bme is None:
            return None
        else:
            return bme.gas

sensors_manager = SensorsManager()
start_new_thread(sensors_manager.sensors_reading, ())