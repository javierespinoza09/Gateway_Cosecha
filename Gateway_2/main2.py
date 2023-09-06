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
#rfm9x = RFM9X()

sio = socketio.Client()


serverInterrupt = False #Variable that stops mainloop if gateway receives a message from server

@sio.event

def reboot():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen(["python3","main.py.","&"])
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
    ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
    print("Acknowledge? {}".format(ack))
    rec = rfm9x.receive(with_ack=True)
    cont = 0
    while rec is not None:
        ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
        print("Acknowledge? {}".format(ack))
        rec = rfm9x.receive(with_ack=True)
        if cont > 10:
            return "Error de comunicación"
        cont += 1

    print(rec)
    return rec


def relays(command, identifier):
    global serverInterrupt
    message = command + identifier
    ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
    print("Acknowledge? {}".format(ack))
    rec = rfm9x.receive(with_ack=True)
    cont = 0
    while rec is None:
        ack = rfm9x.send(message, 0, with_ack=True)  # Send to Node 0
        print("Acknowledge? {}".format(ack))
        rec = rfm9x.receive(with_ack=True)
        if cont > 5:
            serverInterrupt = False
            return "Error de comunicación"
        cont += 1
    serverInterrupt = False
    print(rec)
    
    return "Comando {} se ha enviado correctamente al relay #{}. Info ".format(command, identifier, rec)


def humidity(identifier):
    global serverInterrupt
    dic = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M",
           14: "N", 15: "O"}
    message = "Data!{0}".format(identifier)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    ack = rfm9x.send(message, identifier, with_ack=True)
    print(ack)
    try:
        rec = rfm9x.receive(with_ack=True).split("/")
        print(rec)
        sendurl = {"id_box": dic[identifier], "created_at": dt_string, "sensorA": rec[0], "sensorB": rec[1],
                   "sensorC": rec[2], "sensorD": rec[3], "sensorE": rec[4], "isCalibration": False}
        url = "http://201.207.53.225:3031/api/biocarbon/HumidityReport"
        x = requests.post(url, data=sendurl)
        print(x.text)
        serverInterrupt = False
        return rec
    except:
        print("Error Lectura Caja {}".format(dic[identifier]))
        serverInterrupt = False
        return

def mainLoop():
    global serverInterrupt,rfm9x
    nodes = [9,10,13,14,15] #Cajas a realizar pruebas
    #nodes = [8,9] #Cajas a realizar pruebas
    dic = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 15:"O"}
    
    errors = {}
    for i in range(len(nodes)):
        errors[dic[nodes[i]]] = 0
        
    Good = 0
    Bad = 0
    
    #if(not os.path.exists("/home/pitec/Documents/Biocarbon/RaspGateway/pruebaRSSI.txt")):
        #file = open("/home/pitec/Documents/Biocarbon/RaspGateway/pruebaRSSI.txt", "w")
        #file.write("Caja,RSSI,SNR,Time,Ultima actualizacion\n")
        #file.close()
        
    #if(not os.path.exists("/home/pitec/Documents/Biocarbon/RaspGateway/DatosHumedad.txt")):
        #file = open("/home/pitec/Documents/Biocarbon/RaspGateway/DatosHumedad.txt", "w")
        #file.write("TimeStamp,Caja,Sensor1,Sensor2,Sensor3, Sensor4, Sensor5\n")
        #file.close()
    
    url = "http://201.207.53.225:3031/api/biocarbon/HumidityReport"
    url2 = "http://201.207.53.225:3031/api/biocarbon/TemperatureReport"
    F = 0
    while True:
        if not serverInterrupt:
            now=datetime.now()
            dt_string=now.strftime("%Y-%m-%d %H:%M:%S")
            #fp = open("/home/pitec/Documents/Biocarbon/RaspGateway/pruebaRSSI.txt", 'a')
            #fp2 = open("/home/pitec/Documents/Biocarbon/RaspGateway/DatosHumedad.txt", 'a')
            fp_ = open("/home/pitec/Documents/Biocarbon/RaspGateway/Mediciones.txt", 'w')
            fp_.write("Lecturas totales,Error de lectura,Lectura hecha")
            for i in range(len(nodes)):
                fp_.write(",Errores caja "+dic[nodes[i]])
            fp_.write("\n")
            for node in nodes:
                message = "Data!{0}".format(node)
                t1 = time.time()
                ack = rfm9x.send(message, node, with_ack=True)
                print("Acknowledge? {}".format(ack))
                try:
                    rec = rfm9x.receive(with_ack=True).split("/")
                    print(rec)
                    t2 = time.time()
                    print("tiempo: {}".format(time.time()-t1))
                    sendurl = {"id_box":dic[node], "created_at":dt_string, "sensorA":rec[0], "sensorB":rec[1], "sensorC":rec[2], "sensorD":rec[3], "sensorE":rec[4], "isCalibration":False}
                    #fp.write(str(node) + "," + str(rfm9x.rfm9x.last_rssi) + "," + str(rfm9x.rfm9x.last_snr) +
                    # "," + str(t2-t1) + ","
                    #    + str(dt_string) + "\n")
                    #fp2.write(str(now) + "," + str(node) + "," + str(rec[0]) + "," + str(rec[1]) + "," + str(rec[2]) + "," + str(rec[3]) + "," + str(rec[4])+ "\n")
                    Good += 1
                    x=requests.post(url,data=sendurl)
                    print(x.text)
                    print(sendurl)
                except Exception as e:
                    print("Error Lectura Caja {}. Error: {}".format(dic[node], e))
                    Bad += 1
                    errors[dic[node]] = errors[dic[node]] + 1
                time.sleep(2)
            try:
                ack = rfm9x.send("Temp", 0, with_ack=True)
                print("Acknowledge? {}".format(ack))
                rec = rfm9x.receive(with_ack=True)
                print(rec)
                if rec != None and ack == True:
                    sendurl2 = {"temperature1":rec, "temperature2":2, "temperature3":3, "temperature4":4, "temperature5":5}
                    x = requests.post(url2,data=sendurl2)
                    print("TempSuccess")
                else:
                    print("ErrorTemp")
                    #F = F + 1
                    #if F == 5:
                        #reboot()
            except Exception:
                print("Error Lectura Temp")
            #fp.close()
            #fp2.close()
            fp_.write(str(Good+Bad)+","+str(Bad)+","+str(Good))
            for i in range(len(nodes)):
                fp_.write(","+str(errors[dic[nodes[i]]]))
            fp_.write("\n")
            fp_.close()
        print("Ultima actualizacion: " + str(dt_string))
        time.sleep(40)

try:
    rfm9x = RFM9X()
except Exception:
    reboot()

# Wait until connection is established with server 
while True:
    try:
        x = threading.Thread(target=mainLoop)
        x.start()
        sio.connect('http://201.207.53.225:3031/', transports=['websocket'])
        sio.wait()
        break
    except:
        print("Connection failed. Retrying...")
