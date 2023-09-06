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
        ack = rfm9x.send("Data!77", 77, with_ack=True)
        print("Acknowledge? {}".format(ack))
        rec = rfm9x.receive(with_ack=True)
        if rec != None and ack == True:
            print(rec)   
            print("---")
            return rec
        else:
            print("Error temp")
            return None


try:
    rfm9x = RFM9X()
except Exception:
    reboot()

F = 0


while True:
       
    #try:
    
        dataT = DTemp()    #Se solicita el  dato de temperatura al feather
        time.sleep(3)

        packet = rfm9x.receive(with_ack=True)
        if packet != None:
            if packet == "Temp" and dataT != None:
                print("Dato del Gateway")
                ack = rfm9x.send(dataT, 102, with_ack=True)
                print("Acknowledge? {}".format(ack))          
            else:
                print("Error")
                F = F + 1
                print(F)
                if F == 5:
                    reboot()
                
            
            
            
