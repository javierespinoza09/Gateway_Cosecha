import time
import RPi.GPIO as GPIO
import requests
from datetime import datetime
from RFM9X import RFM9X
rfm9x = RFM9X(node=50)
url = "http://201.207.53.225:3030/api/cosecha/AtmosphericReport"
"""
while True:
    try:
        request = requests.get("http://www.google.com", timeout = 5)
    except (requests.ConnectionError, requests.Timeout):
        print("Sin conexion a internet")
    else:
        print("Con conexion a internet")
        break
url = "http://201.207.53.225:3030/api/cosecha/QualityReport"
"""
while True:
    #pedir =rfm9x.send("Data!23",23,with_ack = True) 
    recibidos = rfm9x.receive(with_ack = True)
    try:
        if recibidos != None and recibidos != "1,":
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            rec = recibidos.split("/")
            recibidos = {"id_device": "1", "created_at": dt_string, "Temperature": rec[0],
                         "Humidity": rec[1], "Pressure": rec[2], "Altitude": rec[3], "Light": rec[4],
                         "Wind direction": rec[5],"Wind speed": rec[6],"Precipitation": rec[7]}
            x = requests.post(url,data = recibidos)
            print(rec)
    except:
        print("Mensaje Desconocido")
       