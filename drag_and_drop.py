import cv2
from cvzone.HandTrackingModule import HandDetector

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
boxes_pos = [[30, 30], [253, 30], [476, 30], [699, 30], [922, 30]]
switch = -1
xdiff, ydiff = 0, 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Placing color boxes in image
    for i in range(5):
        cv2.rectangle(img, (boxes_pos[i][0], boxes_pos[i][1]),
                      ((boxes_pos[i][0]+150), boxes_pos[i][1]+150), (192, 1, 201), -1)

    # Correcting thumb hand
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers[0] == 0:
            fingers[0] = 1
        else:
            fingers[0] = 0

    # Tracing Index and Middle Finger
    lmlist = detector.lmList
    if len(lmlist) > 0:
        if fingers[0] == 0 and fingers[1] == 1 and \
                fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            xp, yp = 0, 0
            x1, y1 = lmlist[8][0], lmlist[8][1]
            x2, y2 = lmlist[12][0], lmlist[12][1]
            length, info = detector.findDistance((x1, y1),
                                                 (x2, y2))
            x3, y3 = (x1 + x2) / 2, (y1 + y2) / 2
            x3, y3 = int(x3), int(y3)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), 2)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            length, info = detector.findDistance((x1, y1), (x2, y2))

            # Selection Mode
            if length < 40:
                for i in range(5):
                    if (x3 < (boxes_pos[i][0]+150)) and (x3 > boxes_pos[i][0]) and \
                            (y3 < (boxes_pos[i][1]+150)) and (y3 > boxes_pos[i][1]):
                        print("Found")
                        if switch == -1:
                            xdiff = x3 - boxes_pos[i][0]
                            ydiff = y3 - boxes_pos[i][1]
                            switch = 0
                        else:
                            boxes_pos[i][0] = x3 - xdiff
                            boxes_pos[i][1] = y3 - ydiff
                        break
            else:
                switch = -1

    # Showing of Image
    cv2.imshow("Video", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
