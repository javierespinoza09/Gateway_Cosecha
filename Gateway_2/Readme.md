# Gateway Cosecha

## Función
Recibir la interrupción del servidor y notificar al módulo de flujo que realize una medición.
- Medición en 2 etapas
> Indicar que se debe tomar una medición (se pueden utilizar 2 variables, una de medicion y una de resultado listo)
> Esperar un tiempo
> Solicitar el dato medido


## API

### URL
#### Post
- http://201.207.53.225:3030/api/cosecha/AtmosphericReport/
- http://201.207.53.225:3030/api/cosecha/QualityReport/

### Formato
#### Atmosférico
sendurl = {"id_device": "1", "Volumen":rec[4],"Precipitacion":rec[6],"Luminosidad":rec[5],"Presion":rec[3],"Vel_Viento":rec[1],"Dir_Viento":rec[2], "Temperatura":rec[2], "Humedad":rec[2]}
#### Flujo
- GET
http://201.207.53.225:3030/api/cosecha/Flow/:command/:id

http://201.207.53.225:3030/api/cosecha/LastFlow/:id

- Post
http://201.207.53.225:3030/api/cosecha/FlowReport/

sendurl={{id_sensor}, ${id_device}, ${flow}}

id_sensor -> Numero del sensor del dispositivo de flujo 

- Put
http://201.207.53.225:3030/api/cosecha/FlowReports
sendurl={{fromdate},{todate},{iddevice}}

