import serial
import time



def turn(amount): # amount in degrees!
    # should write here checking system to know how much it turned_really(encoderinfo,time)

    serR.write('sd'+ str(amount) +'\r')
    ser.write('sd'+ str(amount) +'\r')
def go(amount): # it gets input the pixel difference from the center of the camera.. # should write here checking system to know how much it moved_really - solved with camera feedback
    speedR = amount
    speed = -amount
    serR.write('sd'+ str(speedR) +'\r')
    ser.write('sd'+ str(speed) +'\r')      
def stay():
    serR.write('wl0\r')
    ser.write('wl0\r')

serR = serial.Serial('/dev/ttyACM0',115200, timeout=1) # R always means right motor and without R directs to left motor.
ser = serial.Serial('/dev/ttyACM1',115200, timeout=1)

for i in range(5):
    turn(-12)
    time.sleep(1.5)
    

serR.close()
ser.close()
