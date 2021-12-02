from lib.commandlib import Command, Scheduler
from threading import Thread
import time
from lib.libusbkeys import Keyboard

class KeyboardController:
    __instance = None
    
    VENDOR_ID = 0x04f3
    PRODUCT_ID = 0x0103
    REFRESH_RATE = 0.01
    
    keyboard = Keyboard(VENDOR_ID, PRODUCT_ID)
    
    last_states = {}
    states = {}
    bound_keys = []
    
    last_poll_time = time.time()
    
    for val in keyboard.special_keys.values():
        states[val] = False
        last_states[val] = False
    for val in keyboard.keys.values():
        states[val] = False
        last_states[val] = False
    
    def thread_func(self):
        while True:
            pressed = self.keyboard.getKeys()
            
            for key in self.states.keys():
                if key in pressed:
                    self.states[key] = True
                else:
                    self.states[key] = False
            
            for key in self.bound_keys:
                if key[2]==0 and (not self.last_states[key[0]] and self.states[key[0]]):
                    Scheduler.getInstance().schedule(key[1])
                elif key[2]==1 and (not self.last_states[key[0]] and self.states[key[0]]):
                    Scheduler.getInstance().schedule(key[1])
                elif key[2]==2 and (not self.states[key[0]] and self.last_states[key[0]]):
                    Scheduler.getInstance().schedule(key[1])
                elif key[2]==0 and (not self.states[key[0]] and self.last_states[key[0]]):
                    Scheduler.getInstance().interrupt(key[1])
            
            for key in self.states:
                self.last_states[key] = self.states[key]
            
            current = time.time()
            delay = self.REFRESH_RATE - (current - self.last_poll_time)
            if delay > 0:
                time.sleep(delay)
            self.last_poll_time = current
    
    def whileHeld(self, key:str, comm:Command):
        self.bound_keys.append((key,comm,0))
    
    def whenPressed(self, key:str, comm:Command):
        self.bound_keys.append((key,comm,1))
    
    def whenReleased(self, key:str, comm:Command):
        self.bound_keys.append((key,comm,2))
        
    def getState(self, key:str):
        return self.states[key]
    
    def __init__(self):
        """ Virtually private constructor. """
        if KeyboardController.__instance != None:
                raise Exception("This class is a singleton!")
        else:
                KeyboardController.__instance = self
        
        self.last_poll_time = time.time()
        
        thread = Thread(target=self.thread_func)
        thread.start()
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if KeyboardController.__instance == None:
            KeyboardController()
        return KeyboardController.__instance

if __name__ == "__main__":
    print(KeyboardController.getInstance().states)