#!/usr/bin/python

# Tracking a colored blob in OpenCV
# http://www.aishack.in/2010/07/tracking-colored-objects-in-opencv/

import cv
import time
import serial
# the index of your video feed
# if /dev/videoN is your camera device, then MY_CAMERA = N
MY_CAMERA = 1

def thresholded_image(image):
    # convert image to hsv
    image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)
    # threshold the image (note--I am tracking a blue ball, not a yellow one)
    image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
    orange_min = cv.Scalar(0, 100, 150)
    orange_max = cv.Scalar(255, 200, 255)
#    blue_min = cv.Scalar(255, 200, 160) #orange
#    blue_max = cv.Scalar(255, 111, 0) #orange
    cv.InRangeS(image_hsv, orange_min, orange_max, image_threshed)
    return image_threshed

# use this function to test your thresholds
def test_thresholded_image():
    capture = cv.CaptureFromCAM(MY_CAMERA)
    image = cv.QueryFrame(capture)
    image_threshed = thresholded_image(image)
    cv.NamedWindow('test', cv.CV_WINDOW_AUTOSIZE)
    cv.MoveWindow('test', 100, 100)
    cv.ShowImage('test', image_threshed)
    cv.WaitKey(1000)
    exit(0)

#test_thresholded_image()
def camerainfo():
    # initialize camera feed
    capture = cv.CaptureFromCAM(MY_CAMERA)
    if not capture:
        print "Could not initialize camera feed!"
        exit(1)

    # create display windows
    cv.NamedWindow('camera', cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow('threshed', cv.CV_WINDOW_AUTOSIZE)
    cv.MoveWindow('threshed', 400,  0)

    # holds the tracked position of the ball
    image_scribble = None
    # the position of the ball
    pos_x = 0
    pos_y = 0
    last_x = 0
    last_y = 0
# my creation to find good ball position
    listofxpos = []
    listofypos = []
    ballcoordinates = [0,  0]
    count_of_measurements = 0
    # read from the camera
    print "Tracking ball... press any key to quit"
    while 1:    
        image = cv.QueryFrame(capture)
        if not image:
            return 'no image found'

        # if this is the first frame, we need to initialize it
        if not image_scribble:
            image_scribble = cv.CreateImage(cv.GetSize(image), image.depth, 3)

        # get the thresholded image
        image_threshed = thresholded_image(image)

        # finds the contours in our binary image
        contours = cv.FindContours(cv.CloneImage(image_threshed), cv.CreateMemStorage())
        # if there is a ball in the frame
        if len(contours) != 0:
            # calculate the moments to estimate the position of the ball
            moments = cv.Moments(contours, 1)
            moment10 = cv.GetSpatialMoment(moments, 1, 0)
            moment01 = cv.GetSpatialMoment(moments, 0, 1)
            area = cv.GetCentralMoment(moments, 0, 0)

            # if we got a good enough blob
            if area>1:
                last_x = pos_x
                last_y = pos_y
                pos_x = moment10/area
                pos_y = moment01/area

                print("pos=(%s,%s)"%(pos_x,pos_y))

                # draw the tracking line
                if last_x>0 and last_y>0 and pos_x>0 and pos_y>0:
                    pt1 = (int(last_x), int(last_y))
                    pt2 = (int(pos_x), int(pos_y))
                    cv.Line(image_scribble, pt1, pt2, (0, 255, 255), 5)

        # add the scribble to the original frame
        cv.Add(image, image_scribble, image)
        cv.ShowImage('threshed', image_threshed)
        cv.ShowImage('camera', image)

        # my creation to find good ball position
        if last_x != pos_x or last_y != pos_y:
            if count_of_measurements < 4:
                listofxpos.append(pos_x)
                listofypos.append(pos_y)
                count_of_measurements += 1
            elif count_of_measurements >= 4 and count_of_measurements < 7:# add coordinate selection/filter
                listofxpos.append(pos_x)
                listofypos.append(pos_y)
                count_of_measurements += 1
            elif count_of_measurements >= 7:
                ballcoordinates[0] = sum(listofxpos)/count_of_measurements
                ballcoordinates[1] = sum(listofypos)/count_of_measurements
#                if ballcoordinates[0]  > 200 or ballcoordinates[0] <150: 
#                    amount = (175 - ballcoordinates[0])/5
#                    if amount > 20:
#                        turn(20)
#                    else:
#                        turn(amount)
#                else:
#                    go(20) 
                count_of_measurements = 0
                listofxpos = []
                listofypos = []

            last_x = pos_x
            last_y = pos_y
            print count_of_measurements

# break from the loop if there is a key press
        c = cv.WaitKey(10)
        if not c == -1:
            break
a = '''
def turn(amount): # amount in degrees!
    # should write here checking system to know how much it turned_really(encoderinfo,time)
    serR.write('sd'+ str(amount) +'\r')
    ser.write('sd'+ str(amount) +'\r')
    time.sleep(0.3)
    stay()
def go(amount): # it gets input the pixel difference from the center of the camera.. # should write here checking system to know how much it moved_really - solved with camera feedback
    speedR = amount
    speed = -amount
    serR.write('sd'+ str(speedR) +'\r')
    ser.write('sd'+ str(speed) +'\r')
    time.sleep(1)
    stay()
    
def stay():
    serR.write('wl0\r')
    ser.write('wl0\r')
'''

#serR = serial.Serial('/dev/ttyACM0',115200, timeout=1) # R always means right motor and without R directs to left motor.
#ser = serial.Serial('/dev/ttyACM1',115200, timeout=1)


#go(100)
#time.sleep(1.5)
#turn(23)
#time.sleep(1.5)
#turn(-23)
#time.sleep(1.5)
#stay()
#go(-100,  serR,  ser)

camerainfo()


#serR.close()
#ser.close()
