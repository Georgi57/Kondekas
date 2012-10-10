import cv
import cv2
import serial
import math
import time



def turn(amount): # amount in degrees!
    # should write here checking system to know how much it turned_really(encoderinfo,time)
    serR.write('sd'+ str(amount) +'\r')
    ser.write('sd'+ str(amount) +'\r')
#    print 'turn'
def go(amount): # it gets input the pixel difference from the center of the camera.. # should write here checking system to know how much it moved_really - solved with camera feedback
    speedR = amount
    speed = -amount
    serR.write('sd'+ str(speedR) +'\r')
    ser.write('sd'+ str(speed) +'\r')    
#    print 'go'
def stay():
    serR.write('wl0\r')
    ser.write('wl0\r')
#    print 'stay'

serR = serial.Serial('/dev/ttyACM0',115200, timeout=1) # R always means right motor and without R directs to left motor.
ser = serial.Serial('/dev/ttyACM1',115200, timeout=1)


cv.NamedWindow("webcam", 1)
cv.NamedWindow("hsv_frame", 1)
cv.MoveWindow('webcam', 450, 0)
cam = cv.CaptureFromCAM(1)
pos_x = 0
pos_y = 0
last_x = 0
last_y = 0
# my creation to find good ball position
count_of_measurements = 0
not_found_two_circles = 0
dead_end = 0
last_direction = 1

while True: #0.13
#    measuretime = time.time() # for measuring time
    frame = cv.QueryFrame(cam) # 0.02
    

    #blur the source image to reduce color noise 
    #cv.Smooth(frame, frame, cv.CV_BLUR, 3); 
    
    #convert the image to hsv(Hue, Saturation, Value) so its  
    #easier to determine the color to track(hue) 
    hsv_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)  # 0.003
    cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV) 

    #limit all pixels that don't match our criteria, in this case we are  
    #looking for purple but if you want you can adjust the first value in  
    #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
    #a hue range for the HSV color model 

    
    thresholded_frame =  cv.CreateImage(cv.GetSize(hsv_frame), 8, 1)  # 0.00123s
#    cv.InRangeS(hsv_frame, (0, 80, 0), (30, 255, 255), thresholded_frame)  # works fine during day
#    cv.InRangeS(hsv_frame, (10, 10, 0), (15, 255, 255), thresholded_frame)  # works fine evenings
#    cv.InRangeS(hsv_frame, (10, 150, 0), (25, 255, 255), thresholded_frame)  # works fine evenings2
    cv.InRangeS(hsv_frame, (0, 157, 194), (25, 255, 255), thresholded_frame)  # ANDRES - module for creating constants threshold    
    
    contours = cv.FindContours(cv.CloneImage(thresholded_frame), cv.CreateMemStorage())      # 0.0009
    
    if len(contours)!=0: 
        #determine the objects moments and check that the area is large  
        #enough to be our object 
        moments = cv.Moments(contours,1) 
        moment10 = cv.GetSpatialMoment(moments, 1, 0)
        moment01 = cv.GetSpatialMoment(moments, 0, 1)
        area = cv.GetCentralMoment(moments, 0, 0) 
        
        #there can be noise in the video so ignore objects with small areas 
        if area > 5: 
            #determine the x and y coordinates of the center of the object 
            #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
            pos_x = moment10/area
            pos_y = moment01/area
        
#            print 'x: ' + str(pos_x) + '\ty: ' + str(pos_y) + '\tarea: ' + str(area) 
#            print '*'
            #create an overlay to mark the center of the tracked object 
            overlay = cv.CreateImage(cv.GetSize(frame), 8, 3) 
            
#            cv.Circle(overlay, (int(pos_x), int(pos_y)), 2, (100, 100, 255), 20) 
#            cv.Add(frame, overlay, frame)    
    
#    cv.ShowImage("webcam", frame)                                           # 0.1s
#    cv.ShowImage('hsv_frame',  thresholded_frame)
#    cv.WaitKey(100)
    
    
        # my creation to find good ball position
    if pos_x > 250 or pos_x <100:                                                   # 0.00015 - some occational 6.0...
        dead_end = 0
        amount = (175 - pos_x)*0.1
        if abs(amount) > 10:
            turn(math.copysign(10,  amount))
            last_direction = math.copysign(1, amount) 
        else:
            turn(amount)
            last_direction = math.copysign(1,  amount) 
    else:    
        go(12) 

    if last_x == pos_x or last_y == pos_y:
        not_found_two_circles += 1
    last_x = pos_x
    last_y = pos_y
    
#    if not_found_two_circles > 10:
#        stay()
#        print 'stay'
#        print 'I am staying'
    if not_found_two_circles > 10:
        print 'ball not found, trying to find ball'
#        stay()
        turn(-1 *last_direction*12)
        not_found_two_circles = 0
        dead_end += 1
        last_direction = math.copysign(1,  -1 *last_direction) 
    if dead_end > 50:
        stay()
        print'didn\' find ball'
        break
#    print measuretime - time.time() # for measuring time


serR.close()
ser.close()
