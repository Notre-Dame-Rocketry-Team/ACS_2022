import time
import board
import pulseio

class buzzer:

    def __init__(self):
        self.buzzer = pulseio.PWMOut(board.D6, variable_frequency=False)



    def beep(self,frequency,beeptime): # Set beep time in seconds; Set frequency in Hz
        buzzer.frequency = frequency
        buzzer.duty_cycle = 2**15
        time.sleep(beeptime)
        buzzer.duty_cycle = 0


