# -*- coding: utf-8 -*-
"""HandTracking_Module

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MNH69er7rIiOY0snRtn5IW_zrHqzJDm8
"""

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands = 2,model_complexity=1, detectionConfi = 0.5, trackConfi = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionConfi = detectionConfi
        self.trackConfi = trackConfi

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionConfi,self.trackConfi)
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_drawing_style = mp.solutions.drawing_styles
        self.tipIds = [4,8,12,16,20]

    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for self.handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,self.handLms,self.mpHands.HAND_CONNECTIONS,
                                           self.mpDraw.DrawingSpec(color=(0,0,255),thickness=2, circle_radius=2),
                                           self.mpDraw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
        return img

    def findPosition(self, img, handNo=0, draw=False, id=range(21)):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for ids,lm in enumerate(self.handLms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)

                if ids in id:
                    self.lmList.append([ids,cx,cy])
                    if draw:
                        cv2.circle(img,(cx,cy),10,(0,255,255),cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        fingers = []
        if len(self.lmList)!=0 :
            # Thumb
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            #fingers
            for id in range(1,5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else :
                    fingers.append(0)
        return fingers



def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        sucess, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        # if len(lmList)!=0:
        #     print(lmList[0])
        print(detector.fingersUp())
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255),1)
        cv2.imshow("Img", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()