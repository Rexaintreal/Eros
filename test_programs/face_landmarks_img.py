# this is just a test program im figuring out how to use an image file for the face mesh 


import cv2 
import mediapipe as mp 

mpface=mp.solutions.face_mesh
facemesh=mpface.FaceMesh(static_image_mode=True) 

mpdraw=mp.solutions.drawing_utils    

#loading image from file
img= "examples/mansymm.jpg"
frame=cv2.imread(img) 

if frame is None:    
    print(f"Error: Could not load file")    
    exit()

framergb= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 

#process image
results=facemesh.process(framergb) 

# getting dim 
h,w,c=frame.shape

# resizing image window
max_width = 1000  # maximum width of window
max_height = 700  # maximum height of window 

scale = min(max_width / w, max_height / h, 1)  # keep aspect ratio, only shrink
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
            mpdraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)        
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
            "R Brow": (int(landmarks[righteyebrow].x * w), int(landmarks[righteyebrow].y * h)),        
        }         
        
        # drawing circes and labelling the landmarks on the image         
        for label, (x, y) in points.items():            
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)            
            cv2.putText(frame, label, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            
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

# showing the image
framesize = cv2.resize(frame, (new_w, new_h)) 

cv2.imshow("Image", framesize)
cv2.waitKey(0)
cv2.destroyAllWindows()

