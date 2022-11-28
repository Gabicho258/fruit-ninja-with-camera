import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        # print("Height", height)
        # print("Width", width)
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        # print("Handedness:", results.multi_handedness)
        # print('Hand landmarks:', results.multi_hand_landmarks)
        if results.multi_hand_landmarks is not None:
            index = [12]
            for hand_landmarks in results.multi_hand_landmarks:
                for (i, points) in enumerate(hand_landmarks.landmark):
                    if i in index:
                        x = int(points.x * width)
                        y = int(points.y * height)
                        print("X: ", x)
                        print("Y: ", y)
                # mp_drawing.draw_landmarks(
                #     frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                #     mp_drawing.DrawingSpec(
                #         color=(0, 255, 255), thickness=3, circle_radius=5),
                #     mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=4, circle_radius=5))
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
