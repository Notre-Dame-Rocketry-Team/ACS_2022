import board
import adafruit_icm20x
import adafruit_mpl3115a2
import analogio

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


def init_accelerometer():
    x_axis = analogio.AnalogIn(board.A1)
    y_axis = analogio.AnalogIn(board.A2)
    z_axis = analogio.AnalogIn(board.A3)
    valtuple = (x_axis, y_axis, z_axis)
    x_name = "Acceleometer X acceleration:"
    y_name = "Acceleometer Y acceleration:"
    z_name = "Acceleometer Z acceleration:"
    nametuple = (x_name, y_name, z_name)
    return valtuple, nametuple

def read_accelerometer(valtuple):
    new_tuple = ()
    for val in valtuple: 
         # Convert axis value to float within 0...1 range.
        new_value = val / 65535
        # Shift values to true center (0.5).
        new_value -= 0.5
        # Convert to gravities.
        new_value = new_value * 3.0
        new_tuple.append(new_value)
    acc_x = new_tuple[0] #units: g
    acc_y = new_tuple[1] #units: g
    acc_z = new_tuple[2] #units: g
    return acc_x, acc_y, acc_z

def init_altimeter():
    i2c = board.I2C()
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c)
    altimeter_outputs = ["Pressure","Altitude","Temperature"]
    return altimeter, altimeter_outputs

def read_altimeter(altimeter):
    Pressure = altimeter.pressure
    Altitude = altimeter.altitude
    Temperature = altimeter.temperature
    return Pressure, Altitude, Temperature
