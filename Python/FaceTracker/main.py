import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Imposta il livello di log a 2 (solo errori)

from deepface import DeepFace
import cv2, time, asyncio
import face_recognition
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import dlib
from imutils import face_utils

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

EYE_AR_THRESH = 0.25

# Carica il rilevatore delle espressioni facciali
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r'C:\Users\Acer\OneDrive\Desktop\Programmazione\Esercizi\Python\FaceTracker\shape_predictor_68_face_landmarks.dat')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

    results = hands.process(rgb_frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    async def clear_console():
        await asyncio.sleep(0.2)
        os.system('cls' if os.name=='nt' else 'clear')

    # Rilevamento delle espressioni facciali con dlib
    faces = detector(gray)
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        
        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    #cv2.imshow('Real-time Emotion Detection', frame)
    
    for (top, right, bottom, left), face_landmarks in zip(face_locations, face_landmarks_list):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        left_eye = face_landmarks['left_eye']
        right_eye = face_landmarks['right_eye']
        nose_bridge = face_landmarks['nose_bridge']
        nose_tip = face_landmarks['nose_tip']
        top_lip = face_landmarks['top_lip']
        bottom_lip = face_landmarks['bottom_lip']
        left_eyebrow = face_landmarks['left_eyebrow']
        right_eyebrow = face_landmarks['right_eyebrow']

        leftEAR = eye_aspect_ratio(left_eye)
        rightEAR = eye_aspect_ratio(right_eye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_AR_THRESH:
            cv2.putText(frame, "Occhi Chiusi", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Occhi Aperti", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Disegna il rig per il naso, gli occhi, la bocca e le sopracciglia
        for point in left_eye:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (255, 0, 0), -1)
        
        for point in right_eye:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (255, 0, 0), -1)
        
        for point in nose_bridge:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (255, 0, 255), -1)
        
        for point in nose_tip:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (255, 0, 255), -1)
        
        for point in top_lip:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (0, 255, 0), -1)
        
        for point in bottom_lip:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (0, 255, 0), -1)
        
        for point in left_eyebrow:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (0, 255, 255), -1)
        
        for point in right_eyebrow:
            point = (point[0] * 4, point[1] * 4)
            cv2.circle(frame, point, 2, (0, 255, 255), -1)

        for facial_feature in [left_eye, right_eye, nose_bridge, nose_tip, top_lip, bottom_lip, left_eyebrow, right_eyebrow]:
            for i in range(1, len(facial_feature)):
                cv2.line(frame, (int(facial_feature[i - 1][0] * 4), int(facial_feature[i - 1][1] * 4)), 
                         (int(facial_feature[i][0] * 4), int(facial_feature[i][1] * 4)), (255, 255, 255), 1)


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_max = int(max([landmark.x for landmark in hand_landmarks.landmark]) * frame.shape[1])
            x_min = int(min([landmark.x for landmark in hand_landmarks.landmark]) * frame.shape[1])
            y_max = int(max([landmark.y for landmark in hand_landmarks.landmark]) * frame.shape[0])
            y_min = int(min([landmark.y for landmark in hand_landmarks.landmark]) * frame.shape[0])

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Face, Hand, and Eye Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
