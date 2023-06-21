from datetime import datetime 
import requests
import time
import RPi.GPIO as GPIO
import requests
from RFM9X import RFM9X
rfm9x = RFM9X(node=50)
now = datetime.now()
#dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


url='http://201.207.53.225:3030/api/cosecha/AtmosphericReport/'
urlget="http://201.207.53.225:3030/api/cosecha/LastAtmospheric/"
#url='http://201.207.53.225:3030/api/cosecha/QualityReport/'
#urlget="http://201.207.53.225:3030/api/cosecha/LastQuality/"
response=requests.get(urlget)

while True:
    #pedir =rfm9x.send("Data!23",23,with_ack = True) 
    recibidos = rfm9x.receive(with_ack = True)
    try:
        if recibidos != None and recibidos != "1,":
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            rec = recibidos.split("/")
            #recibidos = {"id_device": 1, "created_at": dt_string, "Temperature": rec[0],
               #          "Humidity": rec[1], "Pressure": rec[2], "Altitude": rec[3], "Light": rec[4],
                #         "Wind direction": rec[5],"Wind speed": rec[6],"Precipitation": rec[7]}
            recibidos = {"id_device": "1", "created_at": dt_string,"UV_Radiation":rec[3],"Flow":rec[5],"Luminosity":rec[4],"Pressure":rec[2],"Temperature":rec[0],"Humidity":rec[1]}
            x = requests.post(url,data = recibidos)
            print(now)
            print(rec)
            #print(recibidos)
            
            print(x.text)

            y=requests.get(urlget)
            print(y.content)
    except:
        print("Mensaje Desconocido")
        
#data = {"id_device":0,"created_at":dt_string,"Flow":'10',"Turbidity":str(2),"DissolvedSolids":str(3),"WaterLevel":str(4),"pH":str(5),"Temperature":str(6),"Conductivity":str(7),"Salinity":str(8)}  
#data = {"id_device":1,"created_at":dt_string,"UV_Radiation":'2',"Flow":'8',"Luminosity":'3',"Pressure":'4',"Temperature":'5',"Humidity":'6'}
#x=requests.post(url,data)    











#if response.status_code==200:
#else:
 #   print("buuu:",response.status_code)
#if response.status_code==200:
 #   print("wuju")
#else:
 #   print("buuu:",response.status_code)   """