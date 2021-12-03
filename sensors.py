import board
import sys
import time
import adafruit_icm20x
import adafruit_bmp3xx
import DFRobot_LIS

# Add DFRobot_LIS import
# LIS_PATH = '/home/pi/repos/DFRobot_LIS/python/raspberrypi'
# sys.path.append(LIS_PATH)


# Payload sensors
import FaBo9Axis_MPU9250

# Constants
TIME_LABEL = ['Time']
ICM_LABELS = ['ICM Acceleration X', 'ICM Acceleration Y', 'ICM Acceleration Z',
              'ICM Gyroscope X',    'ICM Gyroscope Y',    'ICM Gyroscope Z',
              'ICM Magnetometer X', 'ICM Magnetometer Y', 'ICM Magnetometer Z']
LIS_LABELS = ['LIS Acceleration X', 'LIS Acceleration Y', 'LIS Acceleration Z']
BMP_LABELS = ['BMP Pressure',       'BMP Altitude',       'BMP Temperature']
MPU_LABELS = ['MPU Acceleration X']
MPU_LABELS = ['MPU Acceleration X', 'MPU Acceleration Y', 'MPU Acceleration Z',
              'MPU Gyroscope X',    'MPU Gyroscope Y',    'MPU Gyroscope Z',
              'MPU Magnetometer X', 'MPU Magnetometer Y', 'MPU Magnetometer Z']
g = 9.80665


# Timer
def init_time():
    return None, TIME_LABEL


def read_time(_):
    return [time.time()]

# MPU9250
def init_mpu():
    imu = FaBo9Axis_MPU9250.MPU9250()
    imu.configMPU9250(FaBo9Axis_MPU9250.GFS_2000, FaBo9Axis_MPU9250.AFS_16G)

    return imu, MPU_LABELS

def read_mpu(imu):
    try:
        accel = imu.readAccel().values()
    except:
        accel = (0, 0, 0)
    try:
        magn = imu.readMagnet().values()
    except:
        magn = (0, 0, 0)
    try:
        gyro = imu.readGyro().values()
    except:
        gyro = (0, 0, 0)

    return [*accel, *gyro, *magn]

# IMU
def init_imu():
    i2c_imu = board.I2C()  # uses board.SCL and board.SDA
    imu = adafruit_icm20x.ICM20948(i2c_imu)
    imu.accelerometer_range = adafruit_icm20x.AccelRange.RANGE_16G
    imu.MagDataRate = 'RATE_100HZ'
    imu.accelerometer_data_rate = 1125
    imu.gyro_data_rate = 1100
    imu.mag_data_rate = 1125
    imu.accel_dlpf_cutoff = adafruit_icm20x.AccelDLPFFreq.FREQ_473HZ_3DB
    imu.gyro_dlpf_cutoff = adafruit_icm20x.AccelDLPFFreq.DISABLED
    imu.mag_dlpf_cutoff = adafruit_icm20x.AccelDLPFFreq.DISABLED
    # imu.gyro_data_rate_divisor = 200
    # imu.mag_data_rate_divisor = 100

    return imu, ICM_LABELS


def read_imu(imu):
    # each attribute (acceleration,gyro,magnetic) is a tuple (x,y,z) -> Unpacked below.
    t1 = time.time()
    accel = imu.acceleration
    gyro = imu.gyro
    magn = imu.magnetic
    # Acceleration_X = imu.acceleration[0] #Unit: m/s^2
    # Acceleration_Y = imu.acceleration[1] #Unit: m/s^2
    # Acceleration_Z = imu.acceleration[2] #Unit: m/s^2
    # Gyro_X = imu.gyro[0] #Unit: rad/s
    # Gyro_Y = imu.gyro[1] #Unit: rad/s
    # Gyro_Z = imu.gyro[2] #Unit: rad/s
    # Magnetometer_X = imu.magnetic[0] #Unit: µT
    # Magnetometer_Y = imu.magnetic[1] #Unit: µT
    # Magnetometer_Z = imu.magnetic[2] #Unit: µT
    t2 = time.time()
    #print(f'IMU: {t2-t1}')

    # return Acceleration_X, Acceleration_Y, Acceleration_Z, Gyro_X, Gyro_Y, Gyro_Z, Magnetometer_X, Magnetometer_Y, Magnetometer_Z
    return accel + gyro + magn


# Accelerometer
def init_accelerometer():
    '''
    old code
    x_axis = analogio.AnalogIn(board.A1)
    y_axis = analogio.AnalogIn(board.A2)
    z_axis = analogio.AnalogIn(board.A3)
    valtuple = (x_axis, y_axis, z_axis)
    x_name = "Acceleometer X acceleration:"
    y_name = "Acceleometer Y acceleration:"
    z_name = "Acceleometer Z acceleration:"
    nametuple = (x_name, y_name, z_name)
    return valtuple, nametuple
    '''
    # I2C_BUS         = board.I2C()
    I2C_BUS         = 0x01
    ADDRESS_1       = 0x19                   #Sensor address
    acce = DFRobot_LIS.DFRobot_H3LIS200DL_I2C(I2C_BUS, ADDRESS_1)   #accelerometer object

    #Chip initialization
    acce.begin()
    acce.set_range(acce.H3LIS200DL_100G)
    #acce.set_range(acce.LIS331HH_6G)
    acce.set_acquire_rate(acce.NORMAL_400HZ)
    acce.set_filter_mode(acce.SHUTDOWN)

    return acce, LIS_LABELS


def read_accelerometer(accel):
    '''
    Old Code
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
    '''
    t1 = time.time()
    accel_vals = accel.read_acce_xyz()
    accel_vals = [i * g for i in accel_vals]
    t2 = time.time()
    #print(f'Accelerometer: {t2 - t1}')

    return accel_vals


# Altimeter
def init_altimeter():
    # Initialize Altimeter Object
    i2c = board.I2C()
    altimeter = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    altimeter.pressure_oversampling = 1
    altimeter.temperature_oversampling = 1
    altimeter.filter_coefficient = 0

    # Zero out altimeter
    N = 100
    sea_sum = 0
    for _ in range(N):
        sea_sum += altimeter.pressure
        time.sleep(0.01)
    altimeter.sea_level_pressure = sea_sum / N

    return altimeter, BMP_LABELS


def read_altimeter(altimeter):
    t1 = time.time()
    Pressure = altimeter.pressure
    Altitude = altimeter.altitude
    Temperature = altimeter.temperature
    t2 = time.time()
    #print(f'Altimeter: {t2 - t1}')

    return Pressure, Altitude, Temperature
