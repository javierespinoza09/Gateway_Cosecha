#include <List.hpp>

volatile float NumPulsos; //variable para la cantidad de pulsos recibidos
int PinSensor = 2;    //Sensor conectado en el pin 2
float factor_conversion = 5.425    ; //para convertir de frecuencia a caudal
int contador = 0;
float volumenTotal = 0;
float volumen = 0;
int timer=0;
float frecuencia=0;
float flujo =0;
int relayPin = 7; // Define el pin donde está conectado el relay

List<float> list;

void ContarPulsos ()
{
  NumPulsos++;  //incrementamos la variable de pulsos
}

void setup() {
  Serial.begin(9600);       // initialize UART with baud rate of 9600 bps
  pinMode(PinSensor, INPUT);
  attachInterrupt(0, ContarPulsos, RISING); //(Interrupcion 0(Pin2),funcion,Flanco de subida)
  //pinMode(relayPin, OUTPUT); // Configura el pin como salida
}
void loop() {
  
  if (Serial.available() > 0) {
    char data_rcvd = Serial.read();   // read one byte from serial buffer and save to data_rcvd
    //Serial.println(77);
    if (data_rcvd == '1') {
      float f = 0;
      //Serial.println(77);
      for (int i=0; i<10; i++){
        float f = medicion();
        Serial.println(f,4);
      }
      //Serial.println(f,4);
      volumenTotal = 0;
    }
    else{
      float f = 0.0001;
      Serial.println(f,4);
    }
    delay(10000);     
  }
}

float Flujo(){
  float f = 12.34 + 0.0056;
  return f;
}

float medicion  ()
{
  NumPulsos = 0;   //Ponemos a 0 el número de pulsos
  timer= millis();
  //interrupts();    //Habilitamos las interrupciones
  delay(1000);   //muestra de 1 segundo
  //noInterrupts(); //Desabilitamos las interrupciones
  int tiempo = millis()-timer;
  //Serial.print("T: ");
  //Serial.println(tiempo);
 
  frecuencia = NumPulsos; //Hz(pulsos por segundo)
  //Serial.print("0. NumPulsos : ");
  //Serial.println(NumPulsos, 4);
  flujo = frecuencia / factor_conversion; //L/m
  //Serial.print("1. flujo : ");
  //Serial.println(flujo, 4);
  //Serial.print("1.2 Frec");
  //Serial.println(frecuencia, 4);
  volumen = (flujo/60.0)*tiempo/1000.0;
  //Serial.print("2. Volumen x s ");
  //Serial.println(volumen, 4);
  
  volumenTotal = volumenTotal + volumen; //obtenemos el volumen en 1s
  //Serial.print("3. Volumen total: ");
  //Serial.println(volumenTotal, 4);
  volumen =0;
  flujo=0;
  frecuencia=0;
  return volumenTotal;
}
