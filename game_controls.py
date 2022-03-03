import math
import pyautogui

last_position = (None,None)
last_dir = ''

def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    import keyboard
    while True:
    # put your code here
        if keyboard.is_pressed('j')==True:
            pyautogui.press('left')
        elif keyboard.is_pressed('i')==True:
            pyautogui.press('up')
        elif keyboard.is_pressed('k')==True:
            pyautogui.press('down')
        elif keyboard.is_pressed('l')==True:
            pyautogui.press('right')
    
def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        # put your code here
        global last_position
        global last_dir
        if (last_position[0]==None or last_position[1]==None):
            last_position = (x, y)

        else:
            diff_x = x - last_position[0]
            diff_y = y - last_position[1]
            if (abs(diff_x) > 100):
                if (diff_x > 0):
                    pyautogui.press('right')
                    last_dir='right'
                    last_position=(x,y)
                else:
                    pyautogui.press('left')
                    last_dir='left'
                    last_position=(x,y)
            
            elif (abs(diff_y) > 100):
                if (diff_y < 0):
                    pyautogui.press('up')
                    last_dir='up'
                    last_position=(x,y)
                else:
                    pyautogui.press('down')
                    last_dir='down'
                    last_position=(x,y)

        # pass
        

    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = (0,0, 0)
    colorUpper = (350,255,35)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        # your code here
        frame = vs.read()
        flipped = cv2.flip(frame, 1)
        tracker = imutils.resize(flipped, width=600)
        blur = cv2.GaussianBlur(tracker, (5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        color_range = cv2.inRange(hsv, colorLower, colorUpper)
        rid_noise = cv2.erode(color_range, None, iterations=2)
        dilate = cv2.dilate(rid_noise, None, iterations=2)
        contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(len(contours))
        #print("1")
        center = None
        if len(contours[0]) > 0:
            #print("2")
            largest_contour = max(contours[0], key=cv2.contourArea)
            radius = cv2.minEnclosingCircle(largest_contour)
            M = cv2.moments(largest_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            if radius[1] > 10:
                cv2.circle(tracker, (int(radius[0][0]), int(radius[0][1])), int(radius[1]), (0,255,255), 2)
                cv2.circle(tracker, center, 5, (0,255,255), -1)

                pts.appendleft(center)
        
        if num_frames > 10 and len(pts) > 10:
            (dX, dY) = (pts[0][0] - pts[10][0], pts[0][1]-pts[10][1])
            print("3", (dX,dY))
            if (abs(dX) > 30):
                #print("4"3
                if (dX > 30):
                    direction ='right'
                    
                else:
                    direction ='left'                   
            
            elif (abs(dY) >30):
                if (dY < 0):
                    direction = 'up'
                   
                else:
                    direction = 'down'
        cv2.putText(tracker, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        if direction != last_dir:
            if direction == 'right':
                pyautogui.press('right')
                last_dir = 'right'
            elif direction == 'left':
                pyautogui.press('left')
                last_dir = 'left'
            elif direction == 'up':
                pyautogui.press('up')
                last_dir = 'up'
            else:
                pyautogui.press('down')
                last_dir = 'down'

        cv2.imshow('Game Control Window', tracker)
        cv2.waitKey(1)
        num_frames += 1





        continue
        



def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp
    global last_dir
 
    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()
 
    # put your code here
    mp_hand = mp.solutions.hands
    hands = mp_hand.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
 
    drawer = mp.solutions.drawing_utils
 
    direction = ''
 
    while True:
        # your code here
        frame = vs.read()
        flipped = cv2.flip(frame, 1)
        tracker = imutils.resize(flipped, width=600)
        blur = cv2.GaussianBlur(tracker, (5,5),0)
        frame = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
 
        result = hands.process(frame)
 
        landmark_list = []
       
        if result.multi_hand_landmarks != None:
            for multi_hand_landmark in result.multi_hand_landmarks:
                for id, lm in enumerate(multi_hand_landmark.landmark):
                    frame_height = frame.shape[0]
                    frame_width = frame.shape[1]
 
                    x = lm.x * frame_width
                    y = lm.y * frame_height
 
                    #cv2.circle(tracker, (x, y), 3, (255, 0, 255), cv2.FILLED)
 
                    landmark_list.append((id, x, y))
                   
                   
        if len(landmark_list) > 0:
            if landmark_list[4][1] < landmark_list[3][1]:
                print("thumb")
                pyautogui.press('down')
                last_dir = 'down'

            if landmark_list[8][2] < landmark_list[6][2]:
                print("forefinger")
                pyautogui.press('left')
                last_dir = 'left'
            if landmark_list[12][2] < landmark_list[10][2]:
                print("middle")
                pyautogui.press('up')
                last_dir = 'up'
            if landmark_list[16][2] < landmark_list[14][2]:
                print("ring")
            if landmark_list[20][2] < landmark_list[18][2]:
                print("pinky")
                pyautogui.press('right')
                last_dir = 'right'




def main():
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()

if __name__ == '__main__':
	main()
