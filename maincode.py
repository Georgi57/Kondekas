#include
import serial
import time
from Colordetection import *
#the_mother_of_all_functions(yellow)
#the_mother_of_all_functions(blue)

def the_mother_of_all_functions(goal_color): # running code. (like main in c)
    a = 0
    while not a:
        a = find_target_ball()
    go(20)
    time.sleep(0.5)
    stay()
#    ball_to_tribbler()
#    find_goal(goal_color)

# action functions
def find_target_ball(): # find a ball from the camera sight # needed to control whether it is over border or not. # maybe select the nearest ball?
    cam = camerainfo()
    if cam[0] > 200 or cam[0] <150:     #if ball is not is center - calc difference from center
        amount = (175 - camerainfo()[0])/5
        turn(amount)
        time.sleep(0.2)
        stay()
        return False
    else:
        return True
         #some openCV stuff.


def target_ball(): # goal is to get ball approximately to the center of tribbler... to be able with go movement to get the ball.
    return 'yes' # positive scenario
    return find_ball() # negative scenario


def ball_to_tribbler(): # goal is to catch the ball to tribbler; also an unexpected happening needed to code when tribbler doesn't get the ball
    return 'yes' # positive scenario
    return find_ball() # negative scenario


def find_goal(goal_color): # if we find the wrong goal we can do a faste turn
    count = 0
    while check_for_beacon(goal_color) == None or count < 111:
        turn(5, right)
        count += 1
    if count == 111:
        random_move()
        return find_goal()
    return # negative scenario; random_move() > check again

def target_goal(): # depends on communication System
    return None


# passive controls needed to be done
def border_control():
    return None


# camera orders
def detect_ball(): # detect nearest ball?
    return None
def detect_blue_goal(): #maybe needed to target goal?
    return None
def detect_yellow_goal(): #maybe needed to target goal?
    return None
def detect_white_black_border():
    return None



# wheel movement orders # also we can add curved movements (how do we know that robot went where we wanted to_) # PID is recommended if we have time.
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
    
def random_move(): # border_control - Maybe not # small randommove and BIG random move?
    return None

# coilgun movement orders
def score():
    if is_ball_at_tribbler() == None:
        return 'ball not found'
    for i in range(0,4):
        if is_ball_at_tribbler(): # check if ball is gone, if not hit again
            return None
            #initiate IGTP! SHOOT # maybe some waiting period needed for capacitors to load.
    return None

# other sensors
def is_ball_at_tribbler():
    # if sensors don't see ir
    return 'yes' #else: return None

#def check_for_beacon(goal_color): # We won't be using beacon!!!
#    #if you see right wavelength dependent on the color
#    return 'I see' #else: return None


#START
# outfromcorner just a starting code...no function needed.
serR = serial.Serial('/dev/ttyACM0',115200, timeout=1) # R always means right motor and without R directs to left motor.
ser = serial.Serial('/dev/ttyACM1',115200, timeout=1)

#go(100,  serR,  ser)
#time.sleep(1.5)
#turn(23)
#time.sleep(1.5)
#turn(-23)
#time.sleep(1.5)
#stay()
#go(-100,  serR,  ser)

the_mother_of_all_functions(1)

serR.close()
ser.close()

