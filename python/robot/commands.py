from typing import NamedTuple
from lib.commandlib import Command
from robot.subsystems import Arm

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
        self.arm.setVels({self.axis: self.vel})
        print("Command: \"{}\" triggered.".format(self.name))
    
    def exe(self):
        pass
    
    def end(self, is_interrupted:bool):
        self.arm.setVels({self.axis: 0.0})
        print("Command: \"{}\" ended.".format(self.name))
        if is_interrupted:
            print("The command: \"{}\" was interrupted.".format(self.name))
    
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
        print("Command: \"{}\" triggered.".format(self.name))
    
    def exe(self):
        pass
    
    def end(self, is_interrupted:bool):
        self.arm.setVels({self.axis: 0.0})
        print("Command: \"{}\" ended.".format(self.name))
        if is_interrupted:
            print("The command: \"{}\" was interrupted.".format(self.name))
    
    def isFinished(self):
        return True