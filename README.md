# BME280 and Arduino Experiments with Python derivations and implementations for radius of earth and gravitational acceleration plus comparison of varying algorithms for barometric pressure

Plot of gravity and radius with respect to latitude variations:

![Radius and gravitational acceleration as a function of latitude on earth](/radius_gravity_latitude.png)

Wiring the BME280, SD Card, and LiPo Battery for Arduino Data Acquisition:

| Arduino Pin  | BME280 Pin |
| :---: | :---: |
| 5V  | VIN |
| GND | GND |
| A5  | SCK |
| A4  | SDI |
-------------------------------------------
| Arduino Pin  | SD Module Pin |
| :---: | :---: |
| 5V  | VCC  |
| GND | GND  |
| D11 | MOSI |
| D12 | MISO |
| D13 | SCK |

![bme280 wiring for arduino I2C communication](/bme280_arduino_sd_card.png)
