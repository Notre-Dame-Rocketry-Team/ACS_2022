import board
import adafruit_icm20x

def init_imu():
    i2c_imu = board.I2C()  # uses board.SCL and board.SDA
    imu = adafruit_icm20x.ICM20948(i2c_imu)
    imu_outputs = ["Acceleration_X", "Acceleration_Y", "Acceleration_Z", "Gyro_X","Gyro_Y","Gyro_Z","Magnetometer_X","Magnetometer_Y","Magnetometer_Z"]

    return imu, imu_outputs

def read_imu(imu):
    # each attribute (acceleration,gyro,magnetic) is a tuple (x,y,z) -> Unpacked below.
    Acceleration_X = imu.acceleration[0] #Unit: m/s^2
    Acceleration_Y = imu.acceleration[1] #Unit: m/s^2
    Acceleration_Z = imu.acceleration[2] #Unit: m/s^2
    Gyro_X = imu.gyro[0] #Unit: rad/s
    Gyro_Y = imu.gyro[1] #Unit: rad/s
    Gyro_Z = imu.gyro[2] #Unit: rad/s
    Magnetometer_X = imu.magnetic[0] #Unit: µT
    Magnetometer_Y = imu.magnetic[1] #Unit: µT
    Magnetometer_Z = imu.magnetic[2] #Unit: µT

    return Acceleration_X, Acceleration_Y, Acceleration_Z, Gyro_X, Gyro_Y, Gyro_Z, Magnetometer_X, Magnetometer_Y, Magnetometer_Z
