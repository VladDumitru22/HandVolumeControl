import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
PREV_TIME = 0
ACCURACY = 0.8

capture = cv2.VideoCapture(0)
capture.set(3, CAMERA_WIDTH)  #ID 3 is for width
capture.set(4, CAMERA_HEIGHT) #ID 4 is for width

detector = htm.handDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange() # (-65.25, 0.0, 0.03125) arata ca range ul e de la -65->max la 0->min
min_volume = volume_range[0]
max_volume = volume_range[1]
vol = 0
vol_bar = 400
vol_percentage = 0

while True:
    success, image = capture.read() # Citeste un cadru de la camera web si returneaza True la succes si imaginea ca un np_array
    image = cv2.flip(image, 1)
    image = detector.findHands(image)
    landmark_list = detector.findPosition(image, draw=False)
    
    if len(landmark_list):
        #print("Thumb Finger",landmark_list[4],"Index Finger",landmark_list[8])

        x1, y1 = landmark_list[4][1], landmark_list[4][2] #x si y pentru deget mare
        x2, y2 = landmark_list[8][1], landmark_list[8][2] #x si y pentru deget aratator
        cx, cy = (x1+x2)//2, (y1+y2)//2 #gasesc centrul 

        length = math.hypot(x2-x1, y2-y1) #distanta euclidiana de la origine la un punct
        print("Length", length) #300 maximul, 50 minimul

        # Hand range e de la 50 -> 300
        # Volume range e de la -65 -> 0
        if length > 80:  # doar dacă mâna e suficient de aproape
            vol = np.interp(length, [80, 300], [min_volume, max_volume])
            vol_bar = np.interp(length, [80, 300], [400, 150])
            vol_percentage = np.interp(length, [80, 300], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

            # Mov pentru control activ
            cv2.line(image, (x1, y1), (x2, y2), (180, 0, 255), 3)
            cv2.circle(image, (cx, cy), 12, (180, 0, 255), cv2.FILLED)
        else:
            # mâna prea departe -> ignorăm modificarea volumului
            # Roșu pentru mâna prea departe, text portocaliu
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(image, (cx, cy), 12, (0, 0, 255), cv2.FILLED)
            cv2.putText(image, "Too far", (cx - 100, cy - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 140, 255), 2)

    # Bară volum – verde închis margine, verde deschis umplere
    cv2.rectangle(image, (50, 150), (85, 400), (50, 205, 50), 3)
    cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # Text alb pentru procent
    cv2.putText(image, f"{int(vol_percentage)}%", (40, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    curr_time = time.time()
    fps = 1/(curr_time-PREV_TIME)
    PREV_TIME = curr_time

    cv2.putText(image, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 

    cv2.imshow("Gesture Volume", image) # Afiseaza imaginea in fereastra numita 
    cv2.waitKey(1)

    if cv2.getWindowProperty("Gesture Volume", cv2.WND_PROP_VISIBLE) < 1:
        break

capture.release()
cv2.destroyAllWindows()