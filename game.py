import random
import cv2
import HandTrackingModule as htm
import time


def checkWinner(player, comp):
    if player == comp:
        return None
    elif player == 'rock' and comp == 'scissor':
        return 0
    elif player == 'paper' and comp == 'rock':
        return 0
    elif player == 'scissor' and comp == 'paper':
        return 0
    else:
        return 1


# VARIABLES
waitTime = 3
moves = ['rock', 'paper', 'scissor']
scores = [0, 0]  # [player, comp]
comp, player = None, None
wCam, hCam = 1280, 720

# Get feed
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Get detector
detector = htm.handDetector(detectionCon=0.8, maxHands=1)

# Time variables for fps and time limit
pTime = 0
prevTime = time.time()
newTime = time.time()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Drawing centre line, area for input, and scores
    cv2.line(img, (wCam // 2, 0), (wCam // 2, hCam), (0, 0, 0), 5)
    cv2.rectangle(img, (780, 160), (1180, 560), (255, 0, 277), 5)
    cv2.putText(img, f'{scores[1]}', (320, 640), cv2.FONT_HERSHEY_TRIPLEX, 3,
                (20,255,57), 3)
    cv2.putText(img, f'{scores[0]}', (960, 640), cv2.FONT_HERSHEY_TRIPLEX, 3,
                (20,255,57), 3)

    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    # Handling time limit
    if waitTime - int(newTime) + int(prevTime) < 0:
        cv2.putText(img, f'SHOOT!' , (524, 100), cv2.FONT_HERSHEY_TRIPLEX, 2,
                    (0,0,255), 3)
    
    else:
        cv2.putText(img, f'Timer:{waitTime - int(newTime) + int(prevTime)}', (520, 100), cv2.FONT_HERSHEY_TRIPLEX, 1.5,
                    (0,0,226), 3)

    # Hand landmarks obtained, next
    if len(lmList) != 0:

        if newTime - prevTime >= waitTime:

            x, y = lmList[0][1:]

            if 780 < x < 1180 and 160 < y < 560:
                fingers = detector.fingersUp()
                totalFingers = fingers.count(1)

                # Game logic
                if totalFingers == 0:
                    player = 'rock'
                elif totalFingers == 2:
                    player = 'scissor'
                elif totalFingers == 5:
                    player = 'paper'

                comp = moves[random.randint(0, 2)]

                winner = checkWinner(player, comp)
                
                if winner is not None:
                    scores[winner] = scores[winner] + 1
                prevTime = time.time()
                
                
    # Show computer move
    if comp:
        img[160:560, 120:520] = cv2.imread(f'Fingers/{comp}.jpg')


    cv2.putText(img, f'You : {player}', (900,70), cv2.FONT_HERSHEY_TRIPLEX, 1.35, (20,255,57), 3)
    
    cv2.putText(img, f'Comp : {comp}', (100,70), cv2.FONT_HERSHEY_TRIPLEX, 1.35, (20,255,57), 3)
    newTime = time.time()

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
