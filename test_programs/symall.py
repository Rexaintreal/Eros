# trying the facial symmetry analysis on images in a folder and saving results to a text file with dimension and symmetry scores
# using mediapipe face mesh to get landmarks and calculate distances


import cv2
import mediapipe as mp
import math
import os
import glob

mpface=mp.solutions.face_mesh
facemesh=mpface.FaceMesh(static_image_mode=True)

mpdraw=mp.solutions.drawing_utils

# function to analyze single image
def analyze_face_symmetry(img_path):
    frame=cv2.imread(img_path) 
    
    if frame is None:
        return None
    
    framergb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # processing image
    results=facemesh.process(framergb)
    
    # getting dimensions
    h,w,c=frame.shape
    
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
            
            # calculating distances
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
            
            # converting to relative measurements (using eye distance as base unit)
            base_unit = eye_distance
            
            brow_ratio = brow_distance / base_unit
            nose_left_ratio = nose_to_left_eye / base_unit
            nose_right_ratio = nose_to_right_eye / base_unit
            nose_lip_ratio = nose_to_top_lip / base_unit
            lip_ratio = lip_distance / base_unit
            
            # symmetry ratio and scoring
            symmetry_ratio = nose_to_left_eye / nose_to_right_eye if nose_to_right_eye != 0 else 0
            symmetry_percentage = (1 - abs(1 - symmetry_ratio)) * 100
            
            # converting to 1-10 scale 
            if symmetry_percentage >= 95:
                score = 10
            elif symmetry_percentage >= 90:
                score = 9
            elif symmetry_percentage >= 85:
                score = 8
            elif symmetry_percentage >= 80:
                score = 7
            elif symmetry_percentage >= 70:
                score = 6
            elif symmetry_percentage >= 60:
                score = 5
            elif symmetry_percentage >= 50:
                score = 4
            elif symmetry_percentage >= 40:
                score = 3
            elif symmetry_percentage >= 30:
                score = 2
            else:
                score = 1
            
            return {
                'score': score,
                'symmetry_percentage': symmetry_percentage,
                'brow_ratio': brow_ratio,
                'nose_left_ratio': nose_left_ratio,
                'nose_right_ratio': nose_right_ratio,
                'nose_lip_ratio': nose_lip_ratio,
                'lip_ratio': lip_ratio,
                'symmetry_ratio': symmetry_ratio
            }
    
    return None

# getting all image files from examples folder (avoiding duplicates)
image_files = []
processed_files = set()

# check for common image extensions
for ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
    files = glob.glob(f"examples/*.{ext}")
    files.extend(glob.glob(f"examples/*.{ext.upper()}"))
    
    for file in files:
        filename = os.path.basename(file).lower()
        if filename not in processed_files:
            processed_files.add(filename)
            image_files.append(file)

# analyzing all images and saving to text file
with open("face_symmetry_results.txt", "w") as f:
    f.write("Face Symmetry Analysis Results\n")
    f.write("=" * 50 + "\n\n")
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        print(f"Processing {filename}...")
        
        result = analyze_face_symmetry(img_path)
        
        if result:
            f.write(f"{filename} = {result['score']}/10 symm\n")
            f.write(f"  Symmetry Percentage: {result['symmetry_percentage']:.1f}%\n")
            f.write(f"  Brow Width Ratio: {result['brow_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Left Eye: {result['nose_left_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Right Eye: {result['nose_right_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Lip: {result['nose_lip_ratio']:.2f}x eye distance\n")
            f.write(f"  Lip Gap: {result['lip_ratio']:.2f}x eye distance\n")
            f.write(f"  Symmetry Ratio: {result['symmetry_ratio']:.3f}\n")
            f.write("-" * 30 + "\n\n")
        else:
            f.write(f"{filename} = No face detected\n")
            f.write("-" * 30 + "\n\n")

import cv2
import mediapipe as mp
import math
import os
import glob

mpface=mp.solutions.face_mesh
facemesh=mpface.FaceMesh(static_image_mode=True)

mpdraw=mp.solutions.drawing_utils

# function to analyze single image
def analyze_face_symmetry(img_path):
    frame=cv2.imread(img_path) 
    
    if frame is None:
        return None
    
    framergb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # processing image
    results=facemesh.process(framergb)
    
    # getting dimensions
    h,w,c=frame.shape
    
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
            
            # calculating distances
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
            
            # converting to relative measurements (using eye distance as base unit)
            base_unit = eye_distance
            
            brow_ratio = brow_distance / base_unit
            nose_left_ratio = nose_to_left_eye / base_unit
            nose_right_ratio = nose_to_right_eye / base_unit
            nose_lip_ratio = nose_to_top_lip / base_unit
            lip_ratio = lip_distance / base_unit
            
            # symmetry ratio and scoring
            symmetry_ratio = nose_to_left_eye / nose_to_right_eye if nose_to_right_eye != 0 else 0
            symmetry_percentage = (1 - abs(1 - symmetry_ratio)) * 100
            
            # converting to 1-10 scale 
            if symmetry_percentage >= 95:
                score = 10
            elif symmetry_percentage >= 90:
                score = 9
            elif symmetry_percentage >= 85:
                score = 8
            elif symmetry_percentage >= 80:
                score = 7
            elif symmetry_percentage >= 70:
                score = 6
            elif symmetry_percentage >= 60:
                score = 5
            elif symmetry_percentage >= 50:
                score = 4
            elif symmetry_percentage >= 40:
                score = 3
            elif symmetry_percentage >= 30:
                score = 2
            else:
                score = 1
            
            return {
                'score': score,
                'symmetry_percentage': symmetry_percentage,
                'brow_ratio': brow_ratio,
                'nose_left_ratio': nose_left_ratio,
                'nose_right_ratio': nose_right_ratio,
                'nose_lip_ratio': nose_lip_ratio,
                'lip_ratio': lip_ratio,
                'symmetry_ratio': symmetry_ratio
            }
    
    return None

# getting all image files from examples folder (avoiding duplicates)
image_files = []
processed_files = set()

# check for common image extensions
for ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
    files = glob.glob(f"examples/*.{ext}")
    files.extend(glob.glob(f"examples/*.{ext.upper()}"))
    
    for file in files:
        filename = os.path.basename(file).lower()
        if filename not in processed_files:
            processed_files.add(filename)
            image_files.append(file)

# analyzing all images and saving to text file
with open("face_symmetry_results.txt", "w") as f:
    f.write("Face Symmetry Analysis Results\n")
    f.write("=" * 50 + "\n\n")
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        print(f"Processing {filename}...")
        
        result = analyze_face_symmetry(img_path)
        
        if result:
            f.write(f"{filename} = {result['score']}/10 symm\n")
            f.write(f"  Symmetry Percentage: {result['symmetry_percentage']:.1f}%\n")
            f.write(f"  Brow Width Ratio: {result['brow_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Left Eye: {result['nose_left_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Right Eye: {result['nose_right_ratio']:.2f}x eye distance\n")
            f.write(f"  Nose to Lip: {result['nose_lip_ratio']:.2f}x eye distance\n")
            f.write(f"  Lip Gap: {result['lip_ratio']:.2f}x eye distance\n")
            f.write(f"  Symmetry Ratio: {result['symmetry_ratio']:.3f}\n")
            f.write("-" * 30 + "\n\n")
        else:
            f.write(f"{filename} = No face detected\n")
            f.write("-" * 30 + "\n\n")

print("Analysis complete! Results saved to face_symmetry_results.txt")