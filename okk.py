import cv2
import math
import inputkey
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_command_time = 0
command_delay = 0.1
last_command = None
last_space_time = 0
space_delay = 1.0  # 1 second delay for space key

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("sorry bhai Camera error...")
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        co = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x,
                            normalizedLandmark.y,
                            imageWidth, imageHeight)

                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

        current_time = time.time()
        
        # Space key 
        if current_time - last_space_time >= space_delay:
            inputkey.press_key('space')
            last_space_time = current_time
         
        if len(co) == 2:
            xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
            radius = 100
            
            try:
                m = (co[1][1]-co[0][1])/(co[1][0]-co[0][0])
            except:
                continue
                
            a = 1 + m ** 2
            b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
            c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * co[0][0] * m + 2 * m * ym * co[0][0] - 22500
            
            try:
                xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                ya = m * (xa - co[0][0]) + co[0][1]
                yb = m * (xb - co[0][0]) + co[0][1]
            except:
                continue

            if m != 0:
                try:
                    ap = 1 + ((-1/m) ** 2)
                    bp = -2 * xm - 2 * xm * ((-1/m) ** 2) + 2 * (-1/m) * ym - 2 * (-1/m) * ym
                    cp = xm ** 2 + ((-1/m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (-1/m) + 2 * (-1/m) * ym * xm - 22500
                    xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    yap = (-1 / m) * (xap - xm) + ym
                    ybp = (-1 / m) * (xbp - xm) + ym
                except:
                    continue

            cv2.circle(img=image, center=(int(xm), int(ym)), radius=radius, color=(195, 255, 62), thickness=2)
            cv2.circle(img=image, center=(int(xm), int(ym)), radius=radius-10, color=(195, 255, 62), thickness=2)
            cv2.circle(img=image, center=(int(xm), int(ym)), radius=3, color=(0, 255, 255), thickness=-1)
            cv2.line(image, (int(xm-radius), int(ym)), (int(xm+radius), int(ym)), (195, 255, 62), 1)
            cv2.line(image, (int(xm), int(ym-radius)), (int(xm), int(ym+radius)), (195, 255, 62), 1)
            cv2.line(image, (int(xa), int(ya)), (int(xb), int(yb)), (195, 255, 62), 2)

            if current_time - last_command_time >= command_delay:
                if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                    if last_command != "left":
                        inputkey.release_key('s')
                        inputkey.release_key('d')
                        inputkey.press_key('a')
                        print("left jane do")
                        last_command = "left"
                        last_command_time = current_time
                    cv2.putText(image, "left jane do", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 2)

                elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                    if last_command != "left":
                        inputkey.release_key('s')
                        inputkey.release_key('d')
                        inputkey.press_key('a')
                        print("left jane do")
                        last_command = "left"
                        last_command_time = current_time
                    cv2.putText(image, "left jane do", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 2)

                elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                    if last_command != "right":
                        inputkey.release_key('s')
                        inputkey.release_key('a')
                        inputkey.press_key('d')
                        print("right jane do")
                        last_command = "right"
                        last_command_time = current_time
                    cv2.putText(image, "right jane do", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 2)

                elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                    if last_command != "right":
                        inputkey.release_key('s')
                        inputkey.release_key('a')
                        inputkey.press_key('d')
                        print("right jane do")
                        last_command = "right"
                        last_command_time = current_time
                    cv2.putText(image, "right jane do", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 2)
                
                else:
                    if last_command != "forward":
                        inputkey.release_key('s')
                        inputkey.release_key('a')
                        inputkey.release_key('d')
                        inputkey.press_key('w')
                        print("seedha rakh")
                        last_command = "forward"
                        last_command_time = current_time
                    cv2.putText(image, "seedha rakh", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    try:
                        if ybp > yap:
                            cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 2)
                        else:
                            cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 2)
                    except:
                        cv2.line(image, (int(xa), int(ya)), (int(xm), int(ym)), (195, 255, 62), 2)

        elif len(co) == 1:
            if current_time - last_command_time >= command_delay:
                if last_command != "stop":
                    inputkey.release_key('a')
                    inputkey.release_key('d')
                    inputkey.release_key('w')
                    inputkey.press_key('s')
                    print("break lgao")
                    last_command = "stop"
                    last_command_time = current_time
                cv2.putText(image, "break lgao", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.namedWindow('Hand Gesture Control', cv2.WINDOW_NORMAL)
        cv2.imshow('Hand Gesture Control', cv2.flip(image, 1))
      
        cv2.resizeWindow('Hand Gesture Control', 560, 420)
cap.release()
cv2.destroyAllWindows()
