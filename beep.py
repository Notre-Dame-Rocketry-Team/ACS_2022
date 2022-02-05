import time
import board
import pulseio

buzzer = None
def init():
    global buzzer
    buzzer = pulseio.PWMOut(board.D6, variable_frequency=False)

def beep(frequency,beeptime): # Set beep time in seconds; Set frequency in Hz
    global buzzer
    buzzer.frequency = frequency
    buzzer.duty_cycle = 2**15 # ON
    time.sleep(beeptime)
    buzzer.duty_cycle = 0 # OFF


