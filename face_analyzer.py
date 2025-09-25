import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7
)

def dist(a,b): return np.linalg.norm(np.array(a)-np.array(b))
def ratio_score(actual, ideal):
    # harsher scoring: tiny deviations drop points fast
    dev = abs(actual - ideal) / ideal
    if dev <= 0.05: return 10
    if dev <= 0.2:  return 10 * (0.2 - dev) / 0.15
    return 0

L = {"top":10,"brow":9,"nose":2,"chin":152,"left":234,"right":454,
     "eyeL":133,"eyeR":362,"noseL":98,"noseR":327,
     "lipU":13,"lipM":14,"lipL":17}

def brutal_report(img_path: Path) -> str:
    img = cv2.imread(str(img_path))
    if img is None: return "❌ Can't read image."
    h,w,_ = img.shape
    res = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not res.multi_face_landmarks: return "❌ No face detected."

    pts = [(lm.x*w, lm.y*h) for lm in res.multi_face_landmarks[0].landmark]
    p=lambda i: pts[i]

    thirds = [dist(p(L["top"]),p(L["brow"])),
              dist(p(L["brow"]),p(L["nose"])),
              dist(p(L["nose"]),p(L["chin"]))]
    w_face = dist(p(L["left"]),p(L["right"]))
    l_face = dist(p(L["top"]),p(L["chin"]))
    nose_w = dist(p(L["noseL"]),p(L["noseR"]))
    upper_lip = dist(p(L["lipU"]),p(L["lipM"]))
    lower_lip = dist(p(L["lipM"]),p(L["lipL"]))

    thirds_dev = np.mean([abs(x - np.mean(thirds)) / np.mean(thirds) for x in thirds])
    thirds_score = max(0, 20 * (1 - thirds_dev*2))  # harsher
    ratio = l_face / w_face
    face_score = ratio_score(ratio, 1.618) * 5
    sym = 1 - abs((p(L["eyeL"])[0]+p(L["eyeR"])[0])-w)/w
    sym_score = sym * 25
    nose_score = ratio_score(nose_w / w_face, 0.28) * 5
    lip_score = ratio_score(upper_lip/(lower_lip+1e-6), 1/1.6) * 5
    total = np.clip(thirds_score+face_score+sym_score+nose_score+lip_score,0,100)

    return (
        f"⚡ Raw Brutal Report ⚡\n"
        f"Overall harsh score: {total:.1f}/100\n"
        f"Vertical thirds deviation: {thirds_dev:.2f} -> {thirds_score:.1f}/20\n"
        f"Face ratio L/W: {ratio:.2f} -> {face_score:.1f}/5\n"
        f"Symmetry factor: {sym:.2f} -> {sym_score:.1f}/25\n"
        f"Nose width ratio: {nose_w/w_face:.2f} -> {nose_score:.1f}/5\n"
        f"Lip balance ratio: {(upper_lip/(lower_lip+1e-6)):.2f} -> {lip_score:.1f}/5\n"
        "These numbers are raw geometry only. They don't account for aesthetics, expression, hairstyle, makeup, lighting, angle, etc. Use with caution! "
    )
