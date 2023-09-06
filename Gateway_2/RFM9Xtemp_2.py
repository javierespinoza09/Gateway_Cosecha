#from RFM9Xtemp import RFM9X
from RFM9X import RFM9X
import time
import requests
import os
import subprocess


def reboot():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen(["python3","RFM9Xtemp.py","&"])
    
    os._exit(0)
    
def DTemp():
    F = 0
    while F < 10:       
            ack = rfm9x.send("Data!77", 77, with_ack=True)
            print("Acknowledge? {}".format(ack))
            rec = rfm9x.receive(with_ack=True)
            if rec != None and ack == True:
            #print(rec)   
            #print("---")
                return rec
            else:
                print("Error Caja")
                F = F + 1
                print(F)
                #return None
    return None

try:
    rfm9x = RFM9X()
except Exception:
    reboot()

F = 0


while True:   
    try:
        F = 0
        dataT = DTemp()    #Se solicita el  dato de temperatura al feather
        print(dataT)
        while F < 10: 
            packet = rfm9x.receive(with_ack=True)
            print(packet)
            if packet != None and packet == "Temp":
                    print("Dato del Gateway")
                    while J < 10:
                        ack = rfm9x.send("1122", 102, with_ack=True)
                        print("Acknowledge? {}".format(ack))
                        if ack == False:
                            J = J + 1
                        else:
                            break
            else:
                print("Error, empty packet")
                F = F + 1
                print(F)
                
                
    except Exception:
        reboot()
            
            
