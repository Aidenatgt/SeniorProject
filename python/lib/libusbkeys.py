import time
import sys
import time
import usb

class DeviceNotFound(Exception):
   def __init__(self,value):
      self.value = value
   def __str__(self):
      return repr(self.value)
 
class Device:
   def __init__(self, vendor_id, device_id):
      """
      Find and open a USB HID device.
      """
      
      self.vendor_id = vendor_id
      self.device_id = device_id
      self.endpoint = 0x81

      self.device = self.getDevice(vendor_id, device_id)
      
      if self.device == None:
         raise DeviceNotFound("No recognised device connected.")

      self.handle = self.openDevice(self.device)
   
   def __del__(self):
      """
      Releases the device.
      """
      try:
         self.handle.releaseInterface()
         del self.handle
      except:
         pass
   
   def getDevice(self, vendor_id, device_id):
      """
      Searches the USB buses for a device matching the given vendor and device IDs.
      Returns a usb.Device, or None if the device cannot be found.
      """      

      busses = usb.busses()
   
      for bus in busses:
         devices = bus.devices
         for device in devices:
            if device.idVendor == vendor_id and device.idProduct == device_id:
               return device
   
      return None
   
   def openDevice(self, device):
      """
      Opens and claims the specified device. Returns a usb.DeviceHandle
      Also attempts to detach the kernel's driver from the device, if necessary.
      """

      handle = device.open()

      # Attempt to remove other drivers using this device. This is necessary
      # for HID devices.
      try:
         handle.detachKernelDriver(0)
      except:
         pass # Ignore failures here, the device might already be detached.

      handle.claimInterface(0)
      
      return handle

   def getRawData(self):
      data = None
      try:
         data = self.handle.interruptRead(self.endpoint, 8, 0)
      except:
         raise
      return data

class Keyboard(Device):

   special_keys = {0: 'lctrl', 1: 'lshift', 2: 'lalt', 3: 'win', 4: 'rctrl', 5: 'rshift', 6: 'ralt'}

   keys = {41: 'esc', 43: 'tab', 57: 'clock', 44: 'space', 54: ',', 53: '`', 55: '.', 56: '/', 51: ';', 52: "'",
           40: 'enter', 47: '[', 48: ']', 49: '\\', 42: 'bkspace', 45: '-', 46: '=', 70: 'print', 71: 'scrlock',
           72: 'pause', 74: 'home', 77: 'end', 73: 'insert', 75: 'pgup', 76: 'del', 78: 'pgdown', 82: 'up',
           80: 'left', 79: 'right', 81: 'down', 101: 'menu', 83: 'nlock', 84: 'n/', 85: 'n*', 86: 'n-', 87: 'n+',
           88: 'nenter', 99: 'n.', 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i',
           13:'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't',
           24:'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z',  39: '0', 30: '1', 31: '2', 32: '3', 33: '4',
           34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 98: 'n0', 89: 'n1', 90: 'n2', 91: 'n3', 92: 'n4', 93: 'n5',
           94: 'n6', 95: 'n7', 96: 'n8', 97: 'n9'
   }
   
   def usb_to_str(self, usb_data=['0','0','0','0','0','0']):
      for i in range(len(usb_data)):
         usb_data[i]=int(usb_data[i])
      special = usb_data.pop(0)
      del usb_data[0]

      keys_pressed = []

      for i in range(7, -1, -1):
         if special - 2**i >= 0:
            keys_pressed.append(self.special_keys[i])
            special -= 2 ** i

      for i in usb_data:
         if i in self.keys:
            keys_pressed.append(self.keys[i])

      return keys_pressed
   
   def getKeys(self):
      return self.usb_to_str(self.getRawData())
   
if __name__ == "__main__":
   dev = Keyboard(0x04f3, 0x0103)

   while True:
      nums = []
      for i in dev.getKeys():
         nums.append(i)
      print(nums)
      time.sleep(0.1)