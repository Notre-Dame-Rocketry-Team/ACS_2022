"""
PID Control Algorithm v1
  This module will be active only during burnout.
  Note: This program only predicts apogee and recommends a throttle value.
  It does not send commands to actuate the servo (this is done in acs_states.py).
  All units used are SI
"""
# Import modules

import numpy as np
import matplotlib.pyplot as plt
import data_manager
from data_manager import Data_Manager

# Constants
STOP = 0.15 # Use this for servo.throttle() to stop the motor
MAX_UP = -1
MAX_DOWN = 1

# Global Variables
alpha_prev = 0
# theta_prev = 0
t_prev = None
target_throttle = STOP
# Functions
def initialize(manager: Data_Manager):
    manager.add_data(data_manager.Scalar_Data('Projected_Apogee'))
    manager.add_data(data_manager.Scalar_Data('Apogee_Error'))
    manager.add_data(data_manager.Scalar_Data('Alpha'))
    manager.add_data(data_manager.Scalar_Data('target_Throttle'))

def get_dt(in_time):
    global t_prev
    if t_prev == None:
        dt = 0.1
    else:
        dt = in_time - t_prev
    t_prev = in_time
    return dt

def get_dtheta(manager: Data_Manager):
    global theta_prev
    K = 0.7764 # rev/sec
    K = K * (2*np.pi) # rad/sec
    omega = K * (-(float(manager.read_field('servo_Throttle').get_value())) + 0.15)
    t = float(manager.read_field('Time').get_value())
    dt = get_dt(t)
    dtheta = omega*dt
    # print(f"omega: {omega}, dt: {dt}, dtheta: {dtheta}")
    #theta = theta_prev + dtheta
    #theta_prev = theta
    return dtheta

def get_alpha(manager: Data_Manager):#dalpha/dt
    global alpha_prev
    dalpha_dtheta = 2.4464 # [deg/rev]
    dalpha_dtheta = ((dalpha_dtheta/180)*np.pi)/(2*np.pi) # [rad/rad]
    dtheta = get_dtheta(manager)
    dalpha = dalpha_dtheta * dtheta # [rad]
    alpha = alpha_prev + dalpha # [rad]
    alpha_prev = alpha
    manager.update_field('Alpha', alpha)
    # print(f"dalpha: {dalpha}")
    return alpha

def servo_control(manager: Data_Manager):
    t = float(manager.read_field('Time').get_value())
    dt = get_dt(t)
    height = manager.read_field('Kalman_altitude').get_value()
    velocity = manager.read_field('Kalman_velocity').get_value()
    throttle = manager.read_field('servo_Throttle').get_value()

    c = 343  #[m/s] speed of sound
    w_tabs = 1.0*0.0254  # [in to m] tab width
    L_tabs = 6.0*0.0254  # [in to m] max tab length/extension 
    M_e = 736/35.274  # [oz to kg] EMPTY mass of rocket  # [m/s**2] gravity
    launch_angle = 0*np.pi/180 ## [degrees to radians] launch angle
    dt = 0.5  # [s] time step size
    target_apogee = 1463 # [m]

    # Initial conditions for simulation at BURNOUT, initalize variables for in flight
    Vx_R = 0 
    Vy_R = velocity  # [m/s] rocket vertical velocity 
    x_R = 0  # [m] rocket x position
    alt_R = height # [m] rocket altitude
    ## Run Runge Kutta to predict apogee
    Vmag_R = np.sqrt(Vx_R**2 + Vy_R**2) 
    Mach = Vmag_R/c

    extension = np.sin(get_alpha(manager)) * L_tabs
    Cd_o_tabs = 1.28*extension# 10**(0.44*extension - 0.7)
    Cd_tabs = 1/np.sqrt(1-Mach**2)*Cd_o_tabs
    A_tabs = A_tabs = 4*w_tabs*(extension*L_tabs)
    Cd_rocket = 0.45



    if Mach >= 1:
        Mach = 0.99

    # Runge Kutta to predict Apogee from current state
    # update with new sensor data
    VySim = Vy_R 
    VxSim = Vx_R 
    VmagSim = np.sqrt(VySim**2 + VxSim**2)  # magnitude of velocity vector from data
    altSim = alt_R 
    xSim = x_R 

    while VySim > 0:  
        k1vy = dt*fy(VmagSim, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
        k1ry = dt*VySim 
        
        k2vy = dt*fy(VmagSim + 0.5*k1vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
        k2ry = dt*(VySim + k1vy/2)
        
        k3vy = dt*fy(VmagSim + 0.5*k2vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
        k3ry = dt*(VySim + k2vy/2)
        
        k4vy = dt*fy(VmagSim + k3vy, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e) 
        k4ry = dt*(VySim + k3vy)
        
        # Find values at next timeStep
        VySim = VySim + 1.0/6.0*(k1vy + 2.0*k2vy + 2.0*k3vy + k4vy) 
        # VmagSim = np.sqrt(VxSim**2 + VySim**2) 
        VmagSim = VySim
        
        altSim = altSim + 1.0/6.0*(k1ry + 2*k2ry + 2*k3ry + k4ry) 
        
        # Calculate new drag coefficient for tabs/(rocket?)
        Mach = VmagSim/c
        if Mach >= 1.0:
            Mach = 0.99
        Cd_tabs = 1/np.sqrt(1-Mach**2)*Cd_o_tabs 

    SimApogee = altSim 
    error = SimApogee - target_apogee

    ## PID throttle selection
    # if error < 0:
    #     throttle > 0.15  # if simulated apogee is below target, GO DOWN (positive throttle means go down)
    # elif error > 0: 
    #     throttle < 0.15  # if simulated apogee is above target, GO UP (negative throttle means go up)
    # else:
    Kp = 0.00377 # (-(Kp * error)) + 0.15 = -1 when error = 1000ft
    target_throttle = (-(Kp * error)) + 0.15 # Offset of 0.15 because 0.15 denotes 0 (STOP)
    if target_throttle > 1:
        target_throttle = 1
    elif target_throttle < -1:
        target_throttle = -1
    manager.update_field('Projected_Apogee', SimApogee)
    manager.update_field('Apogee_Error', error)
    manager.update_field('target_Throttle', target_throttle)
    return target_throttle

def fy(V, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e):
    rho = 1.225 #[kg/m **3] density of air
    g = 9.80665 # [m/s **2] gravity
    A_rocket = (6.17*0.0254/2)**2*np.pi # [diamter in to m] [m**2]

    Ky = (-0.5*rho*Cd_rocket*V**2*A_rocket*np.cos(launch_angle) - 0.5*rho*Cd_tabs*V**2*A_tabs*np.cos(launch_angle) - M_e*g)/M_e

    return Ky
 
# Unused Function
def fx(V, Cd_rocket, Cd_tabs, A_tabs, launch_angle, M_e):
    rho = 1.225 #[kg/m**3] density of air
    g = 9.81 #[m/s**2] gravity
    A_rocket = (6.17*0.0254/2)**2*np.pi # [diamter in to m] [m**2]

    Kx = (-0.5*rho*Cd_rocket*V**2*A_rocket*np.cos(launch_angle) - 0.5*rho*Cd_tabs*V**2*A_tabs*np.cos(launch_angle))/M_e
    return Kx

