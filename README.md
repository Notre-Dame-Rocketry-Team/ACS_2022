# ACS 2022

This repository contains the code for the 2021-2022 Notre Dame Rocketry
Team (NDRT) Apogee Control System (ACS).

## List of Sensors

| Sensor Type   | Chosen Sensor |
| ------------- | ------------- |
| Altimeter     | BMP390        |
| Accelerometer | ADXL377       |
| IMU           | ICM-20948     |

## Subscale Components

* Read in sensor data
  * Accelerometer
  * Altimeter
  * IMU
* Log sensor readings
* Detect launch/burnout/apogee
* Actuate servo motor

## Connecting to Pi

1. Connect to `ND-guest`
2. Open a terminal
3. Type `ssh pi@strawberry`
4. Enter password `ACS_2022`
