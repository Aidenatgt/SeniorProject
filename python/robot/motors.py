from board import SCL, SDA
import busio
from adafruit_motor.servo import Servo
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
pca.frequency = 50

for chn in pca.channels:
    chn.duty_cycle = 0

class HighTorqueServo(object):
    
    def __init__(self, channel:int):
        self.servo = Servo(pca.channels[channel], min_pulse=460, max_pulse=2560, actuation_range=180)
    
    def set(self, position:float):
        self.servo.angle = position

class NormalServo(object):
    
    def __init__(self, channel:int):
        self.servo = Servo(pca.channels[channel], min_pulse=520, max_pulse=2550, actuation_range=180)
        
    def set(self, position:float):
        self.servo.angle = position