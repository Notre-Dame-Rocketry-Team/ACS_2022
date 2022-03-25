'''
This program produces fake sensor data.
'''
# Import libraries
import csv
import data_manager
from data_manager import Data_Manager

acce = None
altimeter = None
icm = None
times = None

read_row = lambda data, key: [row[key] for row in data]

TIME_VAL     = 'Time'
LIS_ACCEL_X = 'LIS_acceleration_x'
LIS_ACCEL_Y = 'LIS_acceleration_y'
LIS_ACCEL_Z = 'LIS_acceleration_z'
BMP_ALT      = 'BMP_altitude'
ICM_ACCEL_X = 'ICM_acceleration_x'
ICM_ACCEL_Y = 'ICM_acceleration_y'
ICM_ACCEL_Z = 'ICM_acceleration_z'
ICM_GYRO_X = 'ICM_gyroscope_x'
ICM_GYRO_Y = 'ICM_gyroscope_y'
ICM_GYRO_Z = 'ICM_gyroscope_z'
ICM_MAGN_X = 'ICM_magnetometer_x'
ICM_MAGN_Y = 'ICM_magnetometer_y'
ICM_MAGN_Z = 'ICM_magnetometer_z'

def init_time(manager: Data_Manager, rows) -> bool:
    manager.add_data(data_manager.Scalar_Data('Time'))
    global times
    times = iter(read_row(rows, TIME_VAL))
    return True


def read_time(manager: Data_Manager):
    global times
    current_time = next(times)
    manager.update_field('Time', current_time)

def init_imu(manager: Data_Manager, rows) -> bool:
    global icm
    manager.add_data(data_manager.Tuple_Data('ICM_acceleration'))
    manager.add_data(data_manager.Tuple_Data('ICM_gyroscope'))
    manager.add_data(data_manager.Tuple_Data('ICM_magnetometer'))

    icm_accel_x = read_row(rows, ICM_ACCEL_X)
    icm_accel_y = read_row(rows, ICM_ACCEL_Y)
    icm_accel_z = read_row(rows, ICM_ACCEL_Z)
    icm_gyro_x = read_row(rows, ICM_GYRO_X)
    icm_gyro_y = read_row(rows, ICM_GYRO_Y)
    icm_gyro_z = read_row(rows, ICM_GYRO_Z)
    icm_magn_x = read_row(rows, ICM_MAGN_X)
    icm_magn_y = read_row(rows, ICM_MAGN_Y)
    icm_magn_z = read_row(rows, ICM_MAGN_Z)
    icm = iter(zip(icm_accel_x, icm_accel_y, icm_accel_z,
                   icm_gyro_x,  icm_gyro_y,  icm_gyro_z,
                   icm_magn_x,  icm_magn_y,  icm_magn_z))
    return True

def read_imu(manager: Data_Manager):
    data = next(icm)
    accel = data[:3]
    gyro_val = data[3:6]
    magnet_val = data[6:]
    manager.update_field('ICM_acceleration', accel)
    manager.update_field('ICM_gyroscope', gyro_val)
    manager.update_field('ICM_magnetometer', magnet_val)
    # print(f"Acceleration: {accel}")

def init_accelerometer(manager: Data_Manager, rows) -> bool:
    global acce
    manager.add_data(data_manager.Tuple_Data('LIS_acceleration'))
    lis_x = read_row(rows, LIS_ACCEL_X)
    lis_y = read_row(rows, LIS_ACCEL_Y)
    lis_z = read_row(rows, LIS_ACCEL_Z)

    acce = iter(zip(lis_x, lis_y, lis_z))

    return True

def read_accelerometer(manager: Data_Manager):
    try:
        acce = next(acce)
    except:
        acce = [0, 0, 0]
    manager.update_field('LIS_acceleration', acce)

def init_altimeter(manager: Data_Manager, rows) -> bool:
    global altimeter

    manager.add_data(data_manager.Scalar_Data('BMP_altitude'))
    altimeter = iter(read_row(rows, BMP_ALT))

    return True

def read_altimeter(manager: Data_Manager):
    try:
        altitude = next(altimeter)
    except:
        altitude = 0
    manager.update_field('BMP_altitude', altitude)
    # print(f"Altitude: {altitude}")

def initialize_sensors(path: str, manager: Data_Manager) -> bool:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    result = init_time(manager, rows)
    for sensor in manager.active_sensors:
        if sensor == 'IMU':
            result = result and init_imu(manager, rows)
        elif sensor == 'Accelerometer':
            result = result and init_accelerometer(manager, rows)
        elif sensor == 'Altimeter':
            result = result and init_altimeter(manager, rows)
    
    return result

def read_sensors(manager: Data_Manager):
    """
    Author:
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

