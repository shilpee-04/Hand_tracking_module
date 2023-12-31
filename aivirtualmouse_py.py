# -*- coding: utf-8 -*-
"""AIVirtualmouse.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/143IrZjPtGYz96ULcVm5ATQqCD44uf2ZU
"""

import cv2
import mediapipe as md
import time
import math
import HandTrackingModule as hmt
import pyautogui
import numpy as np


def distance(a,b):
    return math.sqrt((a[1]-b[1])**2+(a[2]-b[2])**2)

wcam,hcam = 640,480
scr_width,scr_height = pyautogui.size()

pLocX, pLocY = 0,0
cLocX, pLocY = 0,0
smoothness=5

# print(scr_width,scr_height)

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
cTime=0

detecter = hmt.handDetector()

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)
    detecter.findHands(img)
    lmList = detecter.findPosition(img)
    fingers = detecter.fingersUp()

    if len(lmList)!=0:
        cv2.rectangle(img,(wcam-50,hcam-220),(50,20),(0,255,0),2)
        x2,y2 = lmList[12][1],lmList[12][2]

        cv2.circle(img,(x2,y2),15,(0,255,255))

        x2 = np.interp(x2, (50,wcam-50),(0,scr_width))
        y2 = np.interp(y2, (20,hcam-200),(0,scr_height))
        # print(x2,y2)
        cLocX = pLocX + (x2 - pLocX)/smoothness
        cLocY = pLocY + (y2 - pLocY)/smoothness

        pyautogui.moveTo(cLocX,cLocY)

        pLocX,pLocY = cLocX,cLocY

        if fingers[2]:
            dist_left = int(distance(lmList[8], lmList[12]))
            dist_right = int(distance(lmList[12], lmList[16]))
            # print(dist_left)

            if dist_left > 50:
                # cv2.circle(img,(x2,y2),15,(255,255,0),cv2.FILLED)
                pyautogui.click(button='left')
                pyautogui.sleep(0.5)
            elif dist_right > 50:
                # cv2.circle(img,(x2,y2),15,(255,255,0),cv2.FILLED)
                pyautogui.click(button='right')
                pyautogui.sleep(0.5)
            elif not fingers[0]:
                pyautogui.doubleClick()
                pyautogui.sleep(0.5)



    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS: {int(fps)}',(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)

    cv2.imshow("Img",img)
    cv2.waitKey(1)