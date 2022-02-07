import board
import adafruit_icm20x
import adafruit_bmp3xx
import time
import data_manager
from data_manager import Data_Manager

# Add DFRobot_LIS import
# LIS_PATH = '/home/pi/repos/DFRobot_LIS/python/raspberrypi'
# sys.path.append(LIS_PATH)

import DFRobot_LIS

# Constants
#TIME_LABEL = ['Time']
#ICM_LABELS = ['ICM Acceleration X', 'ICM Acceleration Y', 'ICM Acceleration Z',
#              'ICM Gyroscope X',    'ICM Gyroscope Y',    'ICM Gyroscope Z',
#              'ICM Magnetometer X', 'ICM Magnetometer Y', 'ICM Magnetometer Z']
#LIS_LABELS = ['LIS Acceleration X', 'LIS Acceleration Y', 'LIS Acceleration Z']
#BMP_LABELS = ['BMP Pressure',       'BMP Altitude',       'BMP Temperature']
g = 9.80665

accelerometer = None
altimeter = None
imu = None

# Timer
def init_time(manager: Data_Manager) -> bool:
    manager.add_data(data_manager.Scalar_Data('Time'))
    return True


def read_time(manager: Data_Manager):
    current_time = time.time()
    manager.update_field('Time', current_time) # Time since epoch in s (January 1 1970)


# IMU
def init_imu(manager: Data_Manager) -> bool:
    global imu
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

    manager.add_data(data_manager.Tuple_Data('ICM_acceleration'))
    manager.add_data(data_manager.Tuple_Data('ICM_gyroscope'))
    manager.add_data(data_manager.Tuple_Data('ICM_magnetometer'))

    return True


def read_imu(manager: Data_Manager):
    # each attribute (acceleration,gyro,magnetic) is a tuple (x,y,z) -> Unpacked below.
    #t1 = time.time()
    try:
        accel = imu.acceleration
    except:
        accel = (0,0,0)
    try:
        gyro = imu.gyro
    except:
        gyro = (0,0,0)
    try:
        magn = imu.magnetic
    except:
        magn = (0,0,0)
    # Acceleration_X = imu.acceleration[0] #Unit: m/s^2
    # Acceleration_Y = imu.acceleration[1] #Unit: m/s^2
    # Acceleration_Z = imu.acceleration[2] #Unit: m/s^2
    # Gyro_X = imu.gyro[0] #Unit: rad/s
    # Gyro_Y = imu.gyro[1] #Unit: rad/s
    # Gyro_Z = imu.gyro[2] #Unit: rad/s
    # Magnetometer_X = imu.magnetic[0] #Unit: µT
    # Magnetometer_Y = imu.magnetic[1] #Unit: µT
    # Magnetometer_Z = imu.magnetic[2] #Unit: µT
    #t2 = time.time()
    #print(f'IMU: {t2-t1}')
    manager.update_dict_field('ICM_acceleration', accel) #Unit: m/s^2
    manager.update_dict_field('ICM_gyroscope', gyro) #Unit: rad/s
    manager.update_dict_field('ICM_magnetometer', magn) #Unit: µT
    # return Acceleration_X, Acceleration_Y, Acceleration_Z, Gyro_X, Gyro_Y, Gyro_Z, Magnetometer_X, Magnetometer_Y, Magnetometer_Z
    # return accel + gyro + magn


# Accelerometer
def init_accelerometer(manager: Data_Manager) -> bool:
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
    global accelerometer
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
    manager.add_data(data_manager.Tuple_Data('LIS_acceleration'))

    return True


def read_accelerometer(manager: Data_Manager):
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
    #t1 = time.time()
    try:
        accel_vals = accelerometer.read_acce_xyz()
        accel_vals = [i * g for i in accel_vals]
    except:
        accel_vals = [0,0,0]
    manager.update_field('LIS_acceleration', accel_vals) # Unit: m/s^2 (originally in g)
    #t2 = time.time()
    #print(f'Accelerometer: {t2 - t1}')

    # return accel_vals


# Altimeter
def init_altimeter(manager: Data_Manager) -> bool:
    global altimeter
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
    manager.add_data(data_manager.Scalar_Data('BMP_altitude'))
    manager.add_data(data_manager.Scalar_Data('BMP_pressure'))
    manager.add_data(data_manager.Scalar_Data('BMP_temperature'))

    return True


def read_altimeter(manager: Data_Manager):
    #t1 = time.time()
    try:
        Pressure = altimeter.pressure
    except:
        Pressure = 0
    try:
        Altitude = altimeter.altitude
    except:
        Altitude = 0
    try:
        Temperature = altimeter.temperature
    except:
        Temperature = 0
    manager.update_field('BMP_altitude',Altitude) # in meters
    manager.update_field('BMP_pressure',Pressure) # in hPa
    manager.update_field('BMP_temperature',Temperature) # in °C
    #t2 = time.time()
    #print(f'Altimeter: {t2 - t1}')
    # return Pressure, Altitude, Temperature


def initialize_sensors(manager: Data_Manager) -> bool:
    """
    This function initializes all the sensors
    Note: call other functions in the design
    """
    # Initialize active sensors
    result = init_time(manager)
    for sensor in manager.active_sensors:
        if sensor == 'IMU':
            result = result and init_imu(manager)
        elif sensor == 'Accelerometer':
            result = result and init_accelerometer(manager)
        elif sensor == 'Altimeter':
            result = result and init_altimeter(manager)
    return result

def read_sensors(manager: Data_Manager):
    """
    This function reads relevant values from every
    sensor.
    """
    read_time(manager)
    for sensor in manager.active_sensors:
        if sensor == 'IMU':
            read_imu(manager)
        elif sensor == 'Accelerometer':
            read_accelerometer(manager)
        elif sensor == 'Altimeter':
            read_altimeter(manager)
