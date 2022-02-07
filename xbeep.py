import time
import sys
import board
import pulseio

buzzer = pulseio.PWMOut(board.D6, variable_frequency=True)

buzzer.frequency = sys.argv[1]

OFF = 0
ON = 2**15

buzzer.duty_cycle = ON

time.sleep(sys.argv[2])

buzzer.duty_cycle = OFF


