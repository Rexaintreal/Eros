# simple face recognition with landmarks using webcam eyes, nose , lips , eyebrows etc

#import statements
import cv2
import mediapipe as mp

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

# camera start
cap = cv2.VideoCapture(0)

# error handling
if not cap.isOpened():
    print("Error: Could not open camera")
    print("Make sure your camera is connected and not being used by another app")
    exit()

while True:
    # reading frames from camera 
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # flip image 
    frame = cv2.flip(frame, 1)
    
    # converting color format
    frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # finding faces
    results = face_mesh.process(frame_color)
    
    # getting image dimensions
    h, w, c = frame.shape
    
    # facial landmarks
    left_eye = 33
    right_eye = 362
    nose_tip = 1
    top_lip = 13
    bottom_lip = 14
    left_eyebrow = 70
    right_eyebrow = 296
    
    # check if face is detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            # drawing all face mesh
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face.FACEMESH_CONTOURS,
                None,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )
            
            # extracting specific landmarks
            landmarks = face_landmarks.landmark
            
            # left eye coordinates
            left_eye_x = int(landmarks[left_eye].x * w)
            left_eye_y = int(landmarks[left_eye].y * h)
            
            # right eye coordinates
            right_eye_x = int(landmarks[right_eye].x * w)
            right_eye_y = int(landmarks[right_eye].y * h)
            
            # nose tip coordinates
            nose_x = int(landmarks[nose_tip].x * w)
            nose_y = int(landmarks[nose_tip].y * h)
            
            # top lip coordinates
            top_lip_x = int(landmarks[top_lip].x * w)
            top_lip_y = int(landmarks[top_lip].y * h)
            
            # bottom lip coordinates
            bottom_lip_x = int(landmarks[bottom_lip].x * w)
            bottom_lip_y = int(landmarks[bottom_lip].y * h)
            
            # left eyebrow coordinates
            left_eyebrow_x = int(landmarks[left_eyebrow].x * w)
            left_eyebrow_y = int(landmarks[left_eyebrow].y * h)
            
            # right eyebrow coordinates
            right_eyebrow_x = int(landmarks[right_eyebrow].x * w)
            right_eyebrow_y = int(landmarks[right_eyebrow].y * h)
            
            # drawing circles on specific landmarks
            cv2.circle(frame, (left_eye_x, left_eye_y), 5, (255, 0, 0), -1)  # blue for left eye
            cv2.circle(frame, (right_eye_x, right_eye_y), 5, (255, 0, 0), -1)  # blue for right eye
            cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)  # green for nose
            cv2.circle(frame, (top_lip_x, top_lip_y), 5, (0, 0, 255), -1)  # red for top lip
            cv2.circle(frame, (bottom_lip_x, bottom_lip_y), 5, (0, 0, 255), -1)  # red for bottom lip
            cv2.circle(frame, (left_eyebrow_x, left_eyebrow_y), 5, (255, 255, 0), -1)  # cyan for left eyebrow
            cv2.circle(frame, (right_eyebrow_x, right_eyebrow_y), 5, (255, 255, 0), -1)  # cyan for right eyebrow
            
            # adding labels
            cv2.putText(frame, 'Left Eye', (left_eye_x + 10, left_eye_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'Right Eye', (right_eye_x + 10, right_eye_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'Nose', (nose_x + 10, nose_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'Top Lip', (top_lip_x + 10, top_lip_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'Bottom Lip', (bottom_lip_x + 10, bottom_lip_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'L Brow', (left_eyebrow_x + 10, left_eyebrow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, 'R Brow', (right_eyebrow_x + 10, right_eyebrow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # display frame
    cv2.imshow('Face Landmarks Detection', frame)
    
    # exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# cleanupQ
cap.release()
cv2.destroyAllWindows()
print("Camera released and windows closed")