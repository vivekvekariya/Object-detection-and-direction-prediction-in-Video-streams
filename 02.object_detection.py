import numpy as np
import cv2
from collections import deque
import os
#Initialized for direction fetching.
counter = 0
direction = ""
pts = deque()

def objectdetection(inputpath,mode,signal):
    if signal == 1:
        global pts,counter,direction
        
        if mode == 'webcam':
            capture = cv2.VideoCapture(0) #Capture from Webcam.
        elif mode == 'video':
            capture = cv2.VideoCapture(inputpath) #Class for video capture, constructor for the class.
        else:
            return

        without_background = cv2.createBackgroundSubtractorMOG2()

        #Properties to be passed to video writer. 
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
       
        try: 
            outputpath = inputpath[:-4]+'_out.mp4'
            output = cv2.VideoWriter(outputpath,fourcc, fps, (width,height))
        except:
            outputpath = os.getcwd()+'\output.mp4'
            output = cv2.VideoWriter(outputpath,fourcc, 20, (width,height))

        if (capture.isOpened() == False):
            print('There is error opening video file / starting webcam.')

        while(capture.isOpened()):
            flag,frames = capture.read() #Reads frame by frame.
            masked_frame = without_background.apply(frames)

            final_image,direction = blob_detector(frames,masked_frame)
            final_image = final_image.astype(np.uint8)
            counter += 1

            if flag == True:

                cv2.putText(final_image, direction, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 3)
                cv2.imshow('Object Detection Output',final_image)

                # writes the output frame
                output.write(np.uint8(final_image))

                if frames is None: #Breaks the loop at the last frame.
                    break

                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        capture.release() #Closes videos files.
        output.release()
        cv2.destroyAllWindows()
    else: 
        cv2.destroyAllWindows()


def blob_detector(frames,masked_frame):

    _, binary = cv2.threshold(src=masked_frame, thresh=150, maxval=255, type=cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(image=binary, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    
    if (contours ==[]):
        contours = [(0,0),(0,0)]
    else:
        contours = max(contours, key = cv2.contourArea)  #Keeps maximum area contour.

    try:
        (x,y,w,h) = cv2.boundingRect(contours)
        bounding_box_image = cv2.rectangle(img = frames, pt1 = (x, y), pt2 = (x + w, y + h), color = (255, 0, 0), thickness = 3)
        moments = cv2.moments(contours)
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        
    except:
        bounding_box_image = np.array([0,0])
        center = (0,0)
        
    direction = direction_detector (contours,center)
    
    return bounding_box_image,direction

def direction_detector (contours,center):
    if len(contours)>0:
        pts.appendleft(center)
        direction = ''
        
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore them.
        
        if pts[i - 1] is None or pts[i] is None:
            direction = ''
            continue
            
        
        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 30 and i == 1 and pts[-30] is not None:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-30][0] - pts[i][0]
            dY = pts[-30][1] - pts[i][1]
            (dirX, dirY) = ("", "")

             # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 30:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 30:
                dirY = "North" if np.sign(dY) == 1 else "South"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY
            
            #print(direction)
    
    return direction

if __name__ == "__main__":
    inputpath = r"C:\Users\vivek\Desktop\test.mp4"
    #inputpath = None
    mode = 'video'
    signal = 1
    objectdetection(inputpath,mode,signal)
