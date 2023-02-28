from datetime import datetime 
import requests
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


#url='http://201.207.53.225:3030/api/cosecha/AtmosphericReport/'
#urlget="http://201.207.53.225:3030/api/cosecha/LastAtmospheric/"
url='http://201.207.53.225:3030/api/cosecha/QualityReport/'
urlget="http://201.207.53.225:3030/api/cosecha/LastQuality/"
response=requests.get(urlget)


data = {"id_device":0,"created_at":dt_string,"Flow":'10',"Turbidity":str(2),"DissolvedSolids":str(3),"WaterLevel":str(4),"pH":str(5),"Temperature":str(6),"Conductivity":str(7),"Salinity":str(8)}  
#data = {"id_device":1,"created_at":dt_string,"UV_Radiation":'2',"Flow":'8',"Luminosity":'3',"Pressure":'4',"Temperature":'5',"Humidity":'6'}
x=requests.post(url,data)    

print(x.text)

y=requests.get(urlget)
print(y.content)















#if response.status_code==200:
#else:
 #   print("buuu:",response.status_code)
#if response.status_code==200:
 #   print("wuju")
#else:
 #   print("buuu:",response.status_code)   """