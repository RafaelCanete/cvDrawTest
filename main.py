import cv2
import os
from cvzone.HandTrackingModule import HandDetector

# Vars
width, height = 1280, 720
annotations = [[]]
annotationNumber = -1
annotationStart = False

# frame skipper for delete last annot debounce
frame_skip = 4
frame_counter = 0

# HandDetector
detector = HandDetector(detectionCon= 0.8, maxHands= 1) # Bei 80% Conf. wird eine Hand als Hand gekennzeichnet, Maximale Anzahl and Händen auf 1 gesetzt

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
cv2.setUseOptimized(True)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # flippt das img horizontal

    hands, img = detector.findHands(img) # flipType = False, damit auch bei horizontaler Spiegelung der HD right und left richtig anzeigt
     # cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 1)
    frame_counter += 1


    if hands:
        hand = hands[0] # [0] weil wir nur eine Hand erlaubt haben
        fingers = detector.fingersUp(hand) # Liste mit der Anzahl an gehobenen Fingern
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        indexFinger = lmList[8][0], lmList[8][1]

        print(fingers)

        if fingers == [0,1,1,0,0]: # create pointer index, middlefinger up
            cv2.circle(img, indexFinger, 12, (0,0,255), cv2.FILLED)
    
        if fingers == [0,1,0,0,0]: # Draw pointer
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(img, indexFinger, 12, (0,0,255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        if fingers == [1,1,1,1,1]: # reset drawing
            annotations = [[]]
            annotationNumber = -1
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0] and frame_counter % frame_skip == 0:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                annotationStart = False
            

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(img, annotations[i][j-1], annotations[i][j], (0,0,200), 12)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    # schliesst Webcam wenn man q drückt
    if key == ord("q"):
        break