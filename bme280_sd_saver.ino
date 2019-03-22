#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <math.h>

File datafile; // initialize sd file
const int chipSelect = 4; // CS pin on sd card module

// measurements taken at r_0 (sea level)
const float p_0 = 994.5*100.0;
const float T = 7.0; // input temperature in C
const float dew_pt = -1.0; // input dew pt

// constants related to gravity approx. and rho approx
const float lat = 40.7128; // input latitude
const float phi = lat*(PI/180.0);
const float sin_theta = sin(phi);
const float sin_2theta = sin(2*phi);
const float g_phi = 9.780327+(0.05185921*sq(sin_theta))-(0.0000567*sq(sin_2theta)); // approx. gravity

// constants related to density calculation
const float R_d = 287.05; // dry air gas constant
const float R_v = 461.52; // water vapor gas constant
const float Temp = T+273.15; // temp in K
const float rh = (100.0-(5.0*(T-(dew_pt))))/100.0; // rel humid in fraction form
const float p_sat = 0.61121*exp((18.678-(Temp/234.5))*(Temp/(257.14+Temp)));
const float rho = (p_0/(R_d*Temp))+((rh*p_sat)/(R_v*Temp)); // density calc based on measurements

// coeffs for altitude calc.
const float q = 1.19; // polytropic index
const float q_diff = 1.0-q; 
const float B_coeff = ((p_0)/(rho*g_phi*(q_diff)));

const float L = -0.0065; // temperature lapse rate

Adafruit_BME280 bme; // start BME sensor

void setup() {
    // verify BME280 is working
    bool status;
    status = bme.begin();  
    if (!status) {
        while (1);
    }
    // verify SD card is working
    if (!SD.begin(chipSelect)) {
      return;
    }
}

void loop() {     
    // polytropic calculation
    float pres_ratio = bme.readPressure()/(p_0);
    float z = B_coeff*(1.0-pow(pres_ratio,q_diff));
    // temperature lapse calculation
    float pow_val = (L*R_d)/g_phi;
    float z_lapse = (Temp/L)*(1.0-(pow(pres_ratio,pow_val)));
    
    // SD save section
    String data_array = "";
    data_array += String(millis()); // save milliseconds since start of program
    data_array += ",";
    data_array += String(bme.readTemperature()); // save temp
    data_array += ",";
    data_array += String(bme.readHumidity()); // save humidity
    data_array += ",";
    data_array += String(bme.readPressure()); // save pressure in Pa
    data_array += ",";
    data_array += String(bme.readAltitude(p_0/100.0)); // save altitude from Adafruit routine
    data_array += ",";
    data_array += String(z); // save polytropic altitude calc.

    // SD Card writing and saving
    datafile = SD.open("press5.csv", O_CREAT | O_WRITE);  
    // if the file is valid, write to it:
    if (datafile) {
      datafile.println(data_array); // write data
      datafile.close();
    }
    delay(100);
}
