import socketio
import engineio
from RFM9X import RFM9X
import time
from datetime import datetime
import requests
from datetime import datetime
import threading
import os
rfm9x = RFM9X()

sio = socketio.Client()


serverInterrupt = False #Variable that stops mainloop if gateway receives a message from server

@sio.event
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
    else:
        print("No valid variable data")
        
def flow():
    global serverInterrupt
    serverInterrupt = True
    message = "Flow"
    ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
    print("Acknowledge? {}".format(ack))
    rec = rfm9x.receive(with_ack=True)
    cont = 0
    time.sleep(60)
    while rec is None:
        ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
        print("Acknowledge? {}".format(ack))
        rec = rfm9x.receive(with_ack=True)
        if cont > 100:
            serverInterrupt = False
            return "Error de comunicación"
        cont += 1
    print(rec)
    serverInterrupt = False
    return rec



def mainLoop():
    global serverInterrupt,rfm9x
    nodes = [6,7,10,11,12,13,14] 
    
    url = "http://201.207.53.225:3030/api/cosecha/AtmosphericReport/"
    urlget="http://201.207.53.225:3030/api/cosecha/LastAtmospheric/"
    while True:
        if not serverInterrupt:
            try:
                if recibidos != None and recibidos != "1,":
                    now = datetime.now()
                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                    rec = recibidos.split("/")
                    recibidos = {"id_device": "1", "created_at": dt_string,"UV_Radiation":rec[3],"Flow":rec[5],"Luminosity":rec[4],"Pressure":rec[2],"Temperature":rec[0],"Humidity":rec[1]}
                    x = requests.post(url,data = recibidos)
                    print(now)
                    print(rec)
                    print(x.text)
                    y=requests.get(urlget)
                    print(y.content)
            except:
                print("Mensaje Desconocido")


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
