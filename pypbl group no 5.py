from enum import Flag
import cv2
import time
import os
import handtrackingModule as htm
import pyautogui as p
import time
wCam, hCam = 840, 680

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "pics"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
    # 20:51 remember this time he explain the logic for finger open 
    # 26:01 explain logic for the thumb closing and opening 

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                 fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        # print(totalFingers)

    
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]
       
        if totalFingers == 0:
            p.press("left")
        elif totalFingers==1 :
            p.press("space")
        elif totalFingers==2:
            p.press("space")
        elif totalFingers==3:
            p.press("up")
        elif totalFingers==4:
            p.press("down")
        elif totalFingers==5:
            p.press("right")




    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)