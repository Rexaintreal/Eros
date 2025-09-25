# this is also just a test program to figure out how to check distance between landmarks and do some basic symmetry analysis on an image file



import cv2
import mediapipe as mp

mpface=mp.solutions.face_mesh
facemesh=mpface.FaceMesh(static_image_mode=True)

mpdraw=mp.solutions.drawing_utils

# loading the image file

img = "examples/mansymm.jpg"
frame=cv2.imread(img) 

if frame is None:
    print(f"Error: Could not load file")  
    exit() 

framergb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# processing image

results=facemesh.process(framergb)

# getting dim

h,w,c=frame.shape

# resizing default window size

width = 1000  # maximum width of window
height = 700  # maximum height of window

scale = min(width / w, height / h, 1)  # keep aspect ratio, only shrink
new_w = int(w * scale)
new_h = int(h * scale)

# landmarks 
lefteye=33
righteye=362
nosetip=1
toplip=13
bottomlip=14
lefteyebrow=70
righteyebrow=296

if results.multi_face_landmarks:
    for facelandmarks in results.multi_face_landmarks:
        # drawing face mesh
        mpdraw.draw_landmarks(
            frame, facelandmarks, mpface.FACEMESH_CONTOURS,
            None,
            mpdraw.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1)
        )

        landmarks = facelandmarks.landmark

        # calculating landmark positions 
        points = {
            "Left Eye": (int(landmarks[lefteye].x * w), int(landmarks[lefteye].y * h)),
            "Right Eye": (int(landmarks[righteye].x * w), int(landmarks[righteye].y * h)),
            "Nose": (int(landmarks[nosetip].x * w), int(landmarks[nosetip].y * h)),
            "Top Lip": (int(landmarks[toplip].x * w), int(landmarks[toplip].y * h)),
            "Bottom Lip": (int(landmarks[bottomlip].x * w), int(landmarks[bottomlip].y * h)),
            "L Brow": (int(landmarks[lefteyebrow].x * w), int(landmarks[lefteyebrow].y * h)),
            "R Brow": (int(landmarks[righteyebrow].x * w), int(landmarks[righteyebrow].y * h))
        }   

        # drawing circles on specific landmarks
        for point, coord in points.items():
            cv2.circle(frame, coord, 5, (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, point, (coord[0]+10, coord[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        # adding big text labels for all landmarks
        cv2.putText(frame, "LEFT EYE", (points["Left Eye"][0] - 60, points["Left Eye"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "RIGHT EYE", (points["Right Eye"][0] - 80, points["Right Eye"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "NOSE", (points["Nose"][0] - 40, points["Nose"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "TOP LIP", (points["Top Lip"][0] - 50, points["Top Lip"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "BOTTOM LIP", (points["Bottom Lip"][0] - 70, points["Bottom Lip"][1] + 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "LEFT BROW", (points["L Brow"][0] - 70, points["L Brow"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "RIGHT BROW", (points["R Brow"][0] - 80, points["R Brow"][1] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        
        # calculating distances for symmetry analysis
        import math
        
        # distance between eyes
        eye_distance = math.sqrt((points["Right Eye"][0] - points["Left Eye"][0])**2 + 
                                (points["Right Eye"][1] - points["Left Eye"][1])**2)
        
        # distance between eyebrows 
        brow_distance = math.sqrt((points["R Brow"][0] - points["L Brow"][0])**2 + 
                                 (points["R Brow"][1] - points["L Brow"][1])**2)
        
        # distance from nose to left eye vs nose to right eye (for symmetry)
        nose_to_left_eye = math.sqrt((points["Left Eye"][0] - points["Nose"][0])**2 + 
                                    (points["Left Eye"][1] - points["Nose"][1])**2)
        nose_to_right_eye = math.sqrt((points["Right Eye"][0] - points["Nose"][0])**2 + 
                                     (points["Right Eye"][1] - points["Nose"][1])**2)
        
        # distance from nose to lips
        nose_to_top_lip = math.sqrt((points["Top Lip"][0] - points["Nose"][0])**2 + 
                                   (points["Top Lip"][1] - points["Nose"][1])**2)
        
        # distance between lips
        lip_distance = math.sqrt((points["Bottom Lip"][0] - points["Top Lip"][0])**2 + 
                                (points["Bottom Lip"][1] - points["Top Lip"][1])**2)
        
        # symmetry ratio (should be close to 1.0 for perfect symmetry)
        symmetry_ratio = nose_to_left_eye / nose_to_right_eye if nose_to_right_eye != 0 else 0
        
        # displaying distance measurements on image
        text_y = 30
        cv2.putText(frame, f"Eye Distance: {eye_distance:.1f}px", (10, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.putText(frame, f"Brow Distance: {brow_distance:.1f}px", (10, text_y + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.putText(frame, f"Nose-Left Eye: {nose_to_left_eye:.1f}px", (10, text_y + 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.putText(frame, f"Nose-Right Eye: {nose_to_right_eye:.1f}px", (10, text_y + 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.putText(frame, f"Symmetry Ratio: {symmetry_ratio:.2f}", (10, text_y + 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.putText(frame, f"Nose-Lip Distance: {nose_to_top_lip:.1f}px", (10, text_y + 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # symmetry analysis text
        if 0.95 <= symmetry_ratio <= 1.05:
            symmetry_text = "GOOD SYMMETRY"
            symmetry_color = (0, 255, 0)  # green
        else:
            symmetry_text = "ASYMMETRIC"
            symmetry_color = (0, 0, 255)  # red
            
        cv2.putText(frame, symmetry_text, (10, text_y + 180), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, symmetry_color, 2)

# showing the image
frame_resized = cv2.resize(frame, (new_w, new_h)) 

cv2.imshow("Image", frame_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()