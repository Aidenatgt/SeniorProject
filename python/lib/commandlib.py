from abc import ABC, ABCMeta, abstractmethod
from threading import Thread
import threading
import time

def sole_member(obj, obj_list):
    count = 0
    for member in obj_list:
        if member is obj:
            count += 1
    
    if count > 1:
        for i in range(len(obj_list) - 1):
            if obj_list[i] is obj:
                del obj_list[i]
                count -= 1
            if not (count > 1):
                break
                
        

class Command(ABC, metaclass = ABCMeta):
    
    requirements = []
    
    def __init__(self, name:str):
        self.name = name
    
    def addRequirements(self, *args):
        for req in args:
            self.requirements.append(req)
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def exe(self):
        pass
    
    @abstractmethod
    def end(self, is_interrupted:bool):
        pass
    
    @abstractmethod
    def isFinished(self):
        return True
    
class RunCommand(Command):
    def __init__(self, func):
        self.func = func
    
    def start(self):
        return super().start()
    
    def exe(self):
        self.func()
    
    def end(self, is_interrupted:bool):
        return super().end(is_interrupted)
    
    def isFinished(self):
        return False
    
class InstantCommand(Command):
    def exe(self):
        pass
    
    def end(self, is_interrupted):
        pass
    
    def isFinished(self):
        return True
    
class Subsystem(ABC, metaclass = ABCMeta):
    periodic_duration = 0.02
    
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def periodic(self):
        pass
    
    def thread_func(self):
        last_time = time.time()
        while True:
            self.periodic()
            
            delay = self.periodic_duration - (time.time() - last_time)
            if delay > 0.0:
                time.sleep(delay)
            last_time = time.time()
    
    def __init__(self):
        self.setup()
        thread = Thread(target=self.thread_func)
        thread.start()
    
class Scheduler():
    __instance = None
    
    commands = []
    subsystems = []
    last_run_time = 0.0
    
    cycle_time = 0.01
    
    def thread_iter(self):
        while True:
            current_time = time.time()
            if (current_time - self.last_run_time) >= self.cycle_time :
                for comm in self.commands:
                    comm.exe()
                for comm in self.commands:
                    if comm.isFinished() == True:
                        comm.end(False)
                        try:
                            self.commands.remove(comm)
                        except ValueError:
                            print("the weird thing happened.")
                    
                self.last_run_time = current_time
                
            
                
    def __init__(self):
        """ Virtually private constructor. """
        if Scheduler.__instance != None:
                raise Exception("This class is a singleton!")
        else:
                Scheduler.__instance = self
        self.last_run_time = time.time()
        thread = Thread(target=self.thread_iter)
        thread.start()
    
    def schedule(self, comm:Command):
        comm.start()
        #sole_member(comm,self.commands)
        
        for other in self.commands:
            if not set(other.requirements).isdisjoint(set(comm.requirements)):
                self.interrupt(other)
        self.commands.append(comm)
    
    def interrupt(self, comm:Command):
        if comm in self.commands:
            self.commands.remove(comm)
            comm.end(True)
        
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Scheduler.__instance == None:
            Scheduler()
        return Scheduler.__instance
    
if __name__ == '__main__':
    
    def comm_exe():
        print("test_line")
        
    Scheduler.getInstance().schedule(RunCommand(comm_exe))