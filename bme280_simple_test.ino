#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BME280 bme; // I2C

void setup() {
    Serial.begin(9600);
    if (!bme.begin()) {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }
}


void loop() {
  String vars = "";
  vars += String(bme.readTemperature());
  vars += ",";
  vars += String(bme.readHumidity());
  vars += ",";
  vars += String(bme.readPressure());
  vars += ",";
  vars += String(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.println(vars);
}
