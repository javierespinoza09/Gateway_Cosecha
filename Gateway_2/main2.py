import socketio
import engineio
from RFM9X import RFM9X
import time
from datetime import datetime
import requests
from datetime import datetime
import threading
import os
import subprocess
rfm9x = RFM9X()

sio = socketio.Client()


serverInterrupt = False #Variable that stops mainloop if gateway receives a message from server

@sio.event

def reboot():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen(["python3","main2.py.","&"])
    os._exit(0)

def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.on('Command')
def on_message(data):
    global serverInterrupt
    print('Message: ', data)

    if data == "Flow":
        sio.emit("Result", flow())
    elif "relay" in data:
        serverInterrupt = True
        command = data.split(",")[1]
        id = data.split(",")[2]
        sio.emit("RelayResult", relays(command, id))
    elif "humidity" in data:
        serverInterrupt = True
        id = data.split(",")[1]
        humValues = humidity(int(id))
        if humValues != None:
            sio.emit("HumidityResult", humValues)
        else:
            sio.emit("HumidityResult", "Error")

def flow():
    message = "Flow"
    ack = rfm9x.send("Data!24", 24, with_ack=True)  # Send to Node 0
    print("Acknowledge? {}".format(ack))
    cont = 0
    while ack == 0:
        ack = rfm9x.send("Data!24", 24, with_ack=True)  # Send to Node 0
        print("Acknowledge? {}".format(ack))
        if cont > 5:
            serverInterrupt = False
            return "Error de comunicación"
        cont += 1
    serverInterrupt = False
    return "Comando {} se ha enviado correctamente. Info ".format("Data!24")
    
def mainLoop():
    global serverInterrupt,rfm9x
     
    url_flujo = "http://201.207.53.225:3030/api/cosecha/Flow/"
    url_atmosferico = "http://201.207.53.225:3030/api/cosecha/AtmosphericReport/"
    F = 0
    Flow_good = 0
    Error = 0
    #time.sleep(15)
    #solicitud = flow()
    #print(solicitud)
    while True:
        if not serverInterrupt:
            
            now=datetime.now()
            
            dt_string=now.strftime("%Y-%m-%d %H:%M:%S")
            rec = rfm9x.receive(with_ack=True)
            while rec is None:
                ack = rfm9x.send("Data!24", 24, with_ack=True)  # Send to Node 0
                print("Acknowledge? {}".format(ack))
                #time.sleep(2)
                rec = rfm9x.receive(with_ack=True)
            
            print(rec)
            
        if rec is not None:
            
            rec = rec.split('/')
            
            if rec[0] == "Flujo":
                print(rec[1])
                #sendurl = {"id_box":"Flujo", "created_at":dt_string, "Flujo":rec[1]}
                sendurl={"id_device":"1", "Flujo":rec[1]}
                x = requests.post(url_flujo,data=sendurl)
                print(x.text)
                Flow_good += 1
                
            elif rec[0] == "Estacion":
                print("Dato de la estacion recibido")  
                sendurl = {"id_device": "1", "Volumen":"0","Precipitacion":rec[8],
                           "Luminosidad":rec[5],"Presion":rec[3],"Vel_Viento":rec[7],
                           "Dir_Viento":rec[6],"Temperatura":rec[1], "Humedad":rec[2]}
                x = requests.post(url_atmosferico,data=sendurl)
        
try:
    rfm9x = RFM9X()
    
except Exception:
    reboot() 

# Wait until connection is established with server 
while True:
    try:
        x = threading.Thread(target=mainLoop)
        x.start()
        sio.connect('http://201.207.53.225:3030/', transports=['websocket'])
        sio.wait()
        break
    except:
        print("Connection failed. Retrying...")

