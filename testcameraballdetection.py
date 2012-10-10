import cv
import cv2

cv.NamedWindow("webcam", 1)
cv.NamedWindow("hsv_frame", 1)
cv.MoveWindow('webcam', 450, 0)
cam = cv.CaptureFromCAM(1)
pos_x = 0
pos_y = 0
last_x = 0
last_y = 0

while True:
    
    frame = cv.QueryFrame(cam)
                
    #blur the source image to reduce color noise 
    cv.Smooth(frame, frame, cv.CV_BLUR, 3); 
    
    #convert the image to hsv(Hue, Saturation, Value) so its  
    #easier to determine the color to track(hue) 
    hsv_frame = cv.CreateImage(cv.GetSize(frame), 8, 3) 
    cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV) 
    
    #limit all pixels that don't match our criteria, in this case we are  
    #looking for purple but if you want you can adjust the first value in  
    #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
    #a hue range for the HSV color model 
    thresholded_frame =  cv.CreateImage(cv.GetSize(hsv_frame), 8, 1) 
#    cv.InRangeS(hsv_frame, (0, 80, 0), (30, 255, 255), thresholded_frame)  # works fine during day
#    cv.InRangeS(hsv_frame, (10, 150, 0), (25, 255, 255), thresholded_frame)  # works fine evenings2
#    cv.InRangeS(hsv_frame, (11, 100, 0), (13, 255, 255), thresholded_frame)  # works fine 17:00
    cv.InRangeS(hsv_frame, (0, 157, 194), (25, 255, 255), thresholded_frame)  # ANDRES - module for creating constants threshold
    
    
    contours = cv.FindContours(cv.CloneImage(thresholded_frame), cv.CreateMemStorage())
    
    
    
    
    
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
        
            print 'x: ' + str(pos_x) + '\ty: ' + str(pos_y) + '\tarea: ' + str(area) 
            
            #create an overlay to mark the center of the tracked object 
            overlay = cv.CreateImage(cv.GetSize(frame), 8, 3) 
            
            cv.Circle(overlay, (int(pos_x), int(pos_y)), 2, (100, 100, 255), 20) 
            cv.Add(frame, overlay, frame) 
    
    cv.ShowImage("webcam", frame)
    cv.ShowImage('hsv_frame',  thresholded_frame)
    cv.WaitKey(100)
