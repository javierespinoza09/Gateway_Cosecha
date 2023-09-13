import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_bh1750
import busio
import digitalio
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
# import threading

global lista_conteos
lista_conteos = []
global lista_conteos_dia
lista_conteos_dia = []
global lista_precipitacion_hora
lista_precipitacion_hora = []
global lista_precipitacion_dia
lista_precipitacion_dia = []

# Anemómetro variables
'''
global  speed
global  count_wind_speed
global  wind_speed
global  ban
global  tiempoInicio_viento
'''
speed               = 2.4               # Un tick por segundo equivale a 2.4km/h
count_wind_speed    = 0  # Lleva el conteo de ticks de la velocidad del viento
wind_speed          = 0  # Variable para determinar la velocidad del viento
ban                 = False  # Se establece una bandera para iniciar el conteo
tiempoInicio_viento = time.monotonic()  # Establece el tiempo de inicio del conteo

# Funciones para conteo de ticks del sensor de velocidad de viento
digital_in11        = DigitalInOut(board.D11)    # Lee el pin digital D11

# Funciones para conteo de ticks del sensor de lluvia
digital_in          = DigitalInOut(board.D10)    # Lee el pin digital D10

# Sensor de direccion de viento, variables
analog_in           = AnalogIn(board.A1)         # Lee el pin analogico A1

# I2C BME280
i2c                 = board.I2C()  # uses board.SCL and board.SDA
bme280              = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

# I2C BH1750
i2c                 = board.I2C()
sensor              = adafruit_bh1750.BH1750(i2c)

# Inicializacion UART
uart                = busio.UART(board.TX, board.RX, baudrate=9600)

# Sensor de lluvia variables
'''
global  bucket_size
global  count_hora
global  count_dia
'''
bucket_size         = 0.28  # mm por tick
count_hora          = 0     # Contador de ticks del sensor
count_dia           = 0      # Contador de tickes por día
# Tiempos sensor de lluvia
'''
global  tiempoInicio
global  tiempoInicio_dia
global  tiempoInicio_Sensores
global  condicionSalida
global  condicionSalida_dia
'''
tiempoInicio        = time.monotonic()
tiempoInicio_dia    = time.monotonic()
tiempoInicio_Sensores = time.monotonic()
condicionSalida     = time.monotonic()
condicionSalida_dia = time.monotonic()
i = 1  # Contador de horas, indica la cantidad de horas que ha pasado
k = 1  # Contador de días que han pasado así se sabe que día es
count_hora = 0
lista_conteos.append("Día %d" % k)

def get_voltage_dig_viento(pin):
    return (pin.value * 3.3)

def get_voltage_dig(pin):
    return (pin.value * 3.3)

# Se almacena el valor del pin digital en una variable a
def ticks_viento():  # Va a depender los ticks de lluvia que caigan, es una interrupcion
    dig_wind = get_voltage_dig_viento(digital_in11)
    return dig_wind

def ticks():   # Va a depender los ticks de lluvia que caigan, es una interrupcion
    #global a
    # comp = int(input("Ingrese el valor de a :"))
    a = get_voltage_dig(digital_in)
    return a

def bucket_tipped_hora():  # Contador de los ticks por segundo, para volumen
    global count_hora
    count_hora = count_hora + 1
    print(count_hora)
    time.sleep(1)

def bucket_tipped_dia():  # Contador de los ticks por segundo (volumen)
    global count_dia
    count_dia = count_dia + 1
    print(count_dia)
    time.sleep(1)


# Función del sensor de dirección
def WindDir(value):
    if   (value < 0.23 and value > 0.15):   # 0.21
        return 'ESE 112.5'
    elif (value < 0.29 and value > 0.23):   # 0.27
        return "ENE 67.5"
    elif (value < 0.35 and value > 0.29):   # 0.3
        return "E 90"
    elif (value < 0.45 and value > 0.35):   # 0.41
        return "SSE 157.5"
    elif (value < 0.65 and value > 0.55):   # 0.60
        return "SE 135"
    elif (value < 0.85 and value > 0.75):   # 0.79
        return "SSW 202.5"
    elif (value < 0.98 and value > 0.85):   # 0.93
        return "S 180"
    elif (value < 1.35 and value > 1.25):   # 1.31
        return "NNE 22.5"
    elif (value < 1.55 and value > 1.45):   # 1.49
        return "NE 45"
    elif (value < 1.98 and value > 1.85):   # 1.93
        return "WSW 247.5"
    elif (value < 2.08 and value > 1.98):   # 2.03
        return "SW 225"
    elif (value < 2.31 and value > 2.21):   # 2.26
        return "NNW 337.5"
    elif (value < 2.58  and value > 2.48):  # 2.53
        return "N 0"
    elif (value < 2.72  and value > 2.62):  # 2.67
        return "WNW 292.5"
    elif (value < 2.91  and value > 2.81):  # 2.86
        return "NW 315"
    elif (value < 3.00 and value > 3.15):   # 3.05
        return "W 270"
    else:
        return "0"

# Función para obtener el valor digital de 3.3V de cada tick
def condicionTicks_viento(digital):
    if digital == 3.3:
        ban1 = True
        return ban1
    else:
        ban1 = False
        return ban1

def sensor_velocidad(): # speed,count_wind_speed,wind_speed,ban,tiempoInicio_viento):
    global  speed
    global  count_wind_speed
    global  wind_speed
    global  ban
    global  tiempoInicio_viento
    '''
    global  lista_conteos
    global  lista_conteos_dia
    global  lista_precipitacion_hora
    global  lista_precipitacion_dia
    '''
    if time.monotonic() - tiempoInicio_viento <= 10:
        if (ban == True):
            c = ticks_viento()
            if (c == 0):
                count_wind_speed += 1
                # print(count_wind_speed)
                ban = False

        elif (ban == False):
            c = ticks_viento()
            ban = condicionTicks_viento(c)
    elif time.monotonic() - tiempoInicio_viento > 10:
        wind_speed = (count_wind_speed * speed)/10
        print("La velocidad del viento fue de: %f" %wind_speed, "Km/h")
        count_wind_speed = 0
        tiempoInicio_viento = time.monotonic()

def sensor_precipitacion(): # tiempoInicio,tiempoInicio_dia,tiempoInicio_Sensores,condicionSalida,condicionSalida_dia,bucket_size,count_hora,count_dia):
    global  tiempoInicio
    global  tiempoInicio_dia
    global  tiempoInicio_Sensores
    global  condicionSalida
    global  condicionSalida_dia
    global  bucket_size
    global  count_hora
    global  count_dia
    global  i
    global  k
    if time.monotonic() - tiempoInicio_dia <= 30:
        # Ciclo para tick por hora
        if time.monotonic() - tiempoInicio < 10:
            a = ticks()
            if a == 0:
                bucket_tipped_hora()

        elif time.monotonic() - tiempoInicio_Sensores >= 3:
            #sensores_varios()
            tiempoInicio_Sensores = time.monotonic()


        elif time.monotonic() - condicionSalida >= 10:
            precipitacion_hora = bucket_size*count_hora  # Precipitación por hora
            print("Ya pasaron, ", i , "hora, ", (time.monotonic() - condicionSalida) , "segundos, se va a dejar de contar")
            print("La cantidad de ticks que hubo fueron: ", count_hora)
            print("La precipitación por hora fue de: ", precipitacion_hora , "mm\n")
            count_dia = count_dia + count_hora
            #lista_conteos.append(count_hora)
            count_hora = 0
            i += 1
            tiempoInicio = time.monotonic()

    elif time.monotonic() - condicionSalida_dia > 30:
        print("Ya pasó un día, ", time.monotonic() - condicionSalida, "segundos, se va a dejar de contar")
        count_dia = count_dia + count_hora
        precipitacion_dia = bucket_size*count_dia    # Precipitacion por día
        print("La cantidad de ticks que hubo en el día fueron : ", count_dia)
        print("La precipitación por día fue de: ", precipitacion_dia , "mm")
        #lista_conteos_dia.append("Día %d" % k)
        k += 1
        #lista_conteos.append(count_hora)
        #lista_conteos.append("Día %d" % k)
        #lista_conteos_dia.append(count_dia)
        count_hora = 0
        count_dia = 0
        i = 1
        condicionSalida_dia = time.monotonic()
        condicionSalida = time.monotonic()
        tiempoInicio = time.monotonic()
        tiempoInicio_dia = time.monotonic()
        #print("Ticks cada hora", lista_conteos)
        #print("Ticks cada día", lista_conteos_dia, "\n")

def sensores_varios():
    print("Temperatura: ", bme280.temperature)
    print("Humedad: ", bme280.relative_humidity)
    print("Presión: ", bme280.pressure)
    print("Altitud: ", bme280.altitude)
    print("Luminosidad: ", sensor.lux)
    print("Dirección de viento: ", WindDir(analog_in.value*3.3/65536))
    print("\n")
    data_Temp = uart.write(bytes(f"Temperatura: {bme280.temperature} °C", "ascii"))
    data_Humed = uart.write(bytes(f"\nHumedad: {bme280.relative_humidity} %", "ascii"))
    data_Pres = uart.write(bytes(f"\nPresión: {bme280.pressure} hPa", "ascii"))
    data_Alti = uart.write(bytes(f"\nAltitud: {bme280.altitude} mts", "ascii"))
    data_Lum = uart.write(bytes(f"\nLuminosidad: {sensor.lux} lx", "ascii"))
    data_Direc = uart.write(bytes(f"\nDirección de viento: {WindDir(analog_in.value*3.3/65536)} lx", "ascii"))
    data_Space = uart.write(bytes(f"\n", "ascii"))

while True:
    sensores_varios()
    sensor_velocidad()  # speed,count_wind_speed,wind_speed,ban,tiempoInicio_viento)
    sensor_precipitacion() # tiempoInicio,tiempoInicio_dia,tiempoInicio_Sensores,condicionSalida,condicionSalida_dia,bucket_size,count_hora,count_dia)
