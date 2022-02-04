import time
import board
import pulseio

def init():
    global buzzer
    buzzer = pulseio.PWMOut(board.D6, variable_frequency=False)

def beep(frequency,beeptime): # Set beep time in seconds; Set frequency in Hz
    buzzer.frequency = frequency
    buzzer.duty_cycle = 2**15
    time.sleep(beeptime)
    buzzer.duty_cycle = 0


