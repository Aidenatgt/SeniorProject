# SeniorProject
Aiden Townsend's CHS Senior Project; A large robotic arm.

This code was developed to run on a RaspberryPi Zero using an Adafruit PCA9685 to control the motors.

The code will claim the keyboard with VID_04f3 and PID_0103, and it won't work as a normal keyboard until it's connection is interrupted.

The mini-arm uses PWM servo motors, which the large arm will not use. However, the PLC can read a PWM signal and the RasPi can control the motors in the same way.
This might be computationaly expensive, I haven't done any optimizations yet.

# ToDo
Add a command to detatch the keyboard and end the program.
