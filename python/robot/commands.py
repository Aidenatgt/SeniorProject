from lib.commandlib import Command, InstantCommand
from robot.subsystems import Arm
from lib.keyboard import KeyboardController

class TestCommand(Command):
    def __init__(self, name:str, string:str):
        self.name = name
        self.string = string
    
    def start(self):
        print("{0} Command Started.".format(self.name))
        
    def exe(self):
        print(self.string)
    
    def end(self):
        print("{0} Command Ended.".format(self.name))
    
    def isFinished(self):
        return False

class SetVelocity(Command):
    arm = Arm.getInstance()
    
    def __init__(self, name:str, axis:str, vel:float):
        self.name = name
        self.axis = axis
        self.vel = vel
        self.addRequirements(self.arm)
    
    def start(self):
        if self.axis == 'claw':
            self.arm.setVels({self.axis: self.vel * 90.0})
        else:
            self.arm.setVels({self.axis: self.vel})
        
        print("command started")
    
    def exe(self):
        pass
    
    def end(self, is_interrupted:bool):
        self.arm.setVels({self.axis: 0.0})
    
    def isFinished(self):
        return False

class StopAxis(Command):
    arm = Arm.getInstance()
    
    def __init__(self, name:str, axis:str):
        self.name = name
        self.axis = axis
        self.addRequirements(self.arm)
    
    def start(self):
        self.arm.setVels({self.axis: 0.0})
    
    def exe(self):
        pass
    
    def end(self, is_interrupted:bool):
        self.arm.setVels({self.axis: 0.0})
    
    def isFinished(self):
        return True
    
class ReleaseKeyboard(InstantCommand):
    def start(self):
        kb = KeyboardController.getInstance()
        del kb