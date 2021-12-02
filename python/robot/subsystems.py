from lib.commandlib import Scheduler, Subsystem
from lib.mathlib import Integral, polar_cart
from robot.motors import HighTorqueServo, NormalServo
from constants import min_ang, max_ang, lengths
import math

class PoseOutsideReachException(Exception):
    
    def __init__(self, pose:tuple, message:str="Requested position is outside of the mechanical range"):
        self.pose=pose
        super().__init__(message)
    
    def __str__(self):
        return str(self.pose)

def inverse(endX=0.0, endY=0.0, endZ=0.0, endBeta=0.0, endGamma=0.0):
    try:
        result = [0,0,0,0,0]
        
        endBeta = math.radians(endBeta)
        
        result[4] = 100.0 - endGamma
        
        endH = math.hypot(endX, endY)
        result[0] = math.degrees(math.atan2(endY, endX))
        
        Xtb = -math.cos(endBeta) * lengths[3] + endH
        Ytb = -math.sin(endBeta) * lengths[3] + endZ
        
        Ap = math.atan2(Ytb, Xtb) % math.pi
        Lp = math.hypot(Xtb, Ytb)
        
        Aia = math.acos((lengths[1] ** 2 + Lp ** 2 - lengths[2] ** 2) / (2 * lengths[1] * Lp))
        
        Ada = Aia + Ap if Ytb > 0 else Aia + Ap - math.pi
        Xda = math.cos(Ada) * lengths[1]
        Yda = math.sin(Ada) * lengths[1]
        
        Adb = math.atan2(Ytb - Yda, Xtb - Xda) - Ada if Xtb - Xda > 0.0 else math.atan2(Ytb - Yda, Xtb - Xda) - math.radians(70.0)
        
        Adc = endBeta - (Ada + Adb)
        
        result[1] = math.degrees(Ada)
        result[2] = -math.degrees(Adb)
        result[3] = 150 + math.degrees(Adc)
        
        return result
    except:
        raise PoseOutsideReachException((endX, endY, endZ, endBeta, endGamma))

class Arm(Subsystem):
    __instance = None
    
    vels = {
        'alpha':0.0,
        'beta':0.0,
        'dist':0.0,
        'pitch':0.0,
        'roll':0.0,
        'claw':0.0,
    }
    
    angles = [0, 0, 0, 0, 0, 0]
    
    def setup(self):
        """ Virtually private constructor. """
        if Arm.__instance != None:
                raise Exception("This class is a singleton!")
        else:
                Arm.__instance = self
                
        self.joints = [
            HighTorqueServo(0),
            HighTorqueServo(1),
            HighTorqueServo(2),
            NormalServo(3),
            NormalServo(4),
            NormalServo(5)
        ]
        
        self.alpha_integral = Integral(0.0)
        self.beta_integral = Integral(45.0)
        self.dist_integral = Integral(10.0)
        self.pitch_integral = Integral(0.0)
        self.roll_integral = Integral(0.0)
        self.claw_integral = Integral(135.0)
        self.integrals = [self.alpha_integral, self.beta_integral, self.dist_integral, self.pitch_integral, self.roll_integral, self.claw_integral]
        
    def setAngles(self, angles):
        for i in range(len(self.joints) - 1):
            if i < len(angles):
                if angles[i] > max_ang[i]:
                    angles[i] = max_ang[i]
                    self.integrals[i].set(max_ang[i])
                elif angles[i] < min_ang[i]:
                    angles[i] = min_ang[i]
                    self.integrals[i].set(max_ang[i])
                    
                self.joints[i].set(angles[i])
    
    def setVels(self, set_v:dict):
        for key, value in set_v.items():
            if key in self.vels:
                self.vels[key] = value
    
    def periodic(self):
        self.alpha_integral.update(self.vels['alpha'])
        self.beta_integral.update(self.vels['beta'])
        self.dist_integral.update(self.vels['dist'])
        self.pitch_integral.update(self.vels['pitch'])
        self.roll_integral.update(self.vels['roll'])
        self.claw_integral.update(self.vels['claw'])
        
        end = polar_cart(
            math.radians(self.alpha_integral.get()),
            math.radians(self.beta_integral.get()),
            self.dist_integral.get()
        )
        
        try:
            self.angles = inverse(end[0], end[1], end[2], self.pitch_integral.get(), self.roll_integral.get())
            self.angles.append(self.claw_integral.get())
            self.setAngles(self.angles)
        except PoseOutsideReachException as e:
            print(str(e))
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Arm.__instance == None:
            Arm()
        return Arm.__instance