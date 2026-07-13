#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Definición del mapa de pines corregido
const int pinSensorPulgar  = 36;
const int pinSensorIndice  = 39;
const int pinSensorMedio   = 34;
const int pinSensorAnular  = 35;
const int pinSensorMenique = 32;

// Objeto para controlar el sensor de movimiento espacial
Adafruit_MPU6050 sensorAceleracionInclinacion;

void setup() {
  Serial.begin(115200);

  // Inicializamos el sensor de inclinación interno
  if (!sensorAceleracionInclinacion.begin()) {
    Serial.println("Error: No se detecto el sensor de movimiento en el guante");
    while (1) {
      delay(10);
    }
  }
  // Ajustamos la sensibilidad del acelerómetro
  sensorAceleracionInclinacion.setAccelerometerRange(MPU6050_RANGE_8_G);
}

void loop() {
  // 1. Muestreamos el nivel de flexión de los dedos
  int valorAnalogicoPulgar  = analogRead(pinSensorPulgar);
  int valorAnalogicoIndice  = analogRead(pinSensorIndice);
  int valorAnalogicoMedio   = analogRead(pinSensorMedio);
  int valorAnalogicoAnular  = analogRead(pinSensorAnular);
  int valorAnalogicoMenique = analogRead(pinSensorMenique);

  // 2. Leemos los datos espaciales del guante
  sensors_event_t lecturaAceleracion, lecturaGiroscopio, lecturaIrrelevante;
  sensorAceleracionInclinacion.getEvent(&lecturaAceleracion, &lecturaGiroscopio, &lecturaIrrelevante);

  // 3. Calculamos la inclinación en grados (Pitch y Roll)
  int inclinacionAdelanteAtras = atan2(lecturaAceleracion.acceleration.y, lecturaAceleracion.acceleration.z) * 180.0 / PI;
  int inclinacionIzquierdaDerecha = atan2(-lecturaAceleracion.acceleration.x, lecturaAceleracion.acceleration.z) * 180.0 / PI;

  // 4. Formateamos y enviamos los 7 valores ordenados (Dedos + Inclinación)
  Serial.print(valorAnalogicoPulgar);  Serial.print(",");
  Serial.print(valorAnalogicoIndice);  Serial.print(",");
  Serial.print(valorAnalogicoMedio);   Serial.print(",");
  Serial.print(valorAnalogicoAnular);  Serial.print(",");
  Serial.print(valorAnalogicoMenique); Serial.print(",");
  Serial.print(inclinacionAdelanteAtras); Serial.print(",");
  Serial.println(inclinacionIzquierdaDerecha); // Cierre de línea

  // Muestreo constante para evitar lag
  delay(20);
}
 