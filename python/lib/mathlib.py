import time
import math

def cart_polar(x=0.0, y=0.0, z=0.0):
    result = [0.0, 0.0, 0.0]
    result[0] = math.atan2(y, x)
    result[1] = math.atan2(z, math.hypot(x, y))
    result[2] = (x ** 2 + y ** 2 + z ** 2) ** 0.5
    return result

def polar_cart(alpha = 0.0, beta = 0.0, dist = 0.0):
    result = [0.0, 0.0, 0.0]
    
    result[2] = math.sin(beta) * dist
    horiz = math.cos(beta) * dist
    result[1] = math.sin(alpha) * horiz
    result[0] = math.cos(alpha) * horiz
    
    return result

class Integral(object):
    
    def __init__(self, c):
        self.val = c
        self.last_time = time.time()
    
    def update(self, value:float):
        self.val += value * (time.time() - self.last_time)
        self.last_time = time.time()
    
    def get(self):
        return self.val
    
    def set(self, val:float):
        self.val = val