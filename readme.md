# Eros - Face Geometry Analyzer

A raw facial geometry analyzer that measures your face against mathematical beauty standards. Built with Flask, OpenCV, and MediaPipe because I was curious about the science behind facial attractiveness.

## What it does

Analyzes faces using actual research formulas:
- Rule of thirds (face divided into equal parts)
- Golden ratio proportions (1.618)
- Facial symmetry measurements
- Nose width ratios
- Lip proportion analysis

Gives you a brutal 0-100 score based purely on geometry.

## The Science

This uses real research from actual scientists:

**Marquardt (2002)** - Found that attractive faces follow the golden ratio (1.618)
**Farkas et al. (1985)** - Measured thousands of faces to find ideal proportions
**Rhodes et al. (1998)** - Proved that symmetry equals attractiveness
**Powell & Humphreys (1984)** - Mapped out the "perfect" face ratios

### Key Formulas

**Rule of Thirds:**
```python
# Face should split into 3 equal parts
hairline_to_eyebrows = eyebrows_to_nose = nose_to_chin
deviation = how far off from perfect thirds
score = 20 points max
```

**Golden Ratio:**
```python
face_length / face_width should equal 1.618
upper_lip / lower_lip should equal 1/1.6
actual_ratio compared to ideal_ratio = points
```

**Symmetry:**
```python
left_eye_position vs right_eye_position
perfect_center = face_width / 2
symmetry_score = how close to perfect center
```

**Nose Analysis:**
```python
nose_width / face_width should equal 0.28
deviation from 0.28 = point deduction
```

## Project Structure

```
eros/
├── app.py              # Flask server
├── face_analyzer.py    # All the math happens here
├── static/
│   ├── assets/
│   │   ├── logo.png
│   │   └── upload.svg
│   ├── uploads/        # temp image storage
│   └── style.css
├── templates/
│   ├── index.html      # upload page
│   └── result.html     # results page
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/yourusername/eros.git
cd eros
pip install -r requirements.txt
python app.py
```

Go to localhost:5000

## Live Demo

Check it out: [erosweb.pythonanywhere.com](https://erosweb.pythonanywhere.com)

## Requirements

```txt
Flask==2.3.3
opencv-python==4.8.1.78
mediapipe==0.10.7
numpy==1.24.3
Pillow==10.0.1
```

## How it works

1. MediaPipe detects 468 facial landmarks
2. Calculates distances between key points
3. Compares measurements to research-backed ideal ratios
4. Harsh scoring system - small deviations lose points fast
5. Gives you the raw numbers

### The Brutal Scoring

```python
def ratio_score(actual, ideal):
    deviation = abs(actual - ideal) / ideal
    if deviation <= 0.05: return 10      # perfect
    if deviation <= 0.2:  return 10 * (0.2 - deviation) / 0.15
    return 0  # you're cooked
```

### Landmark Points Used

```python
landmarks = {
    "top": 10,        # hairline
    "brow": 9,        # eyebrow center
    "nose": 2,        # nose tip
    "chin": 152,      # chin bottom
    "left": 234,      # face left edge
    "right": 454,     # face right edge
    "eyeL": 133,      # left eye center
    "eyeR": 362,      # right eye center
    "noseL": 98,      # nose left
    "noseR": 327,     # nose right
    "lipU": 13,       # upper lip
    "lipM": 14,       # lip center
    "lipL": 17        # lower lip
}
```

## Sample Analysis

```
Raw Brutal Report
Overall harsh score: 67.3/100
Vertical thirds deviation: 0.15 -> 14.0/20
Face ratio L/W: 1.45 -> 6.5/5
Symmetry factor: 0.89 -> 22.3/25
Nose width ratio: 0.31 -> 3.2/5
Lip balance ratio: 0.58 -> 4.8/5
```

## Important Notes

This only measures geometry. It doesn't care about:
- Skin quality
- Eye color
- Hair
- Makeup
- Lighting
- Camera angle
- Facial expression
- Personal style

The scoring is intentionally harsh because tiny deviations from "perfect" proportions drop your score fast.

## Limitations

- Based on Western beauty standards
- Needs clear front-facing photos
- MediaPipe sometimes misses landmarks
- Beauty is way more complex than math
- Don't take this too seriously

## Contributing

If you want to add features or fix bugs, just fork it and make a pull request. Keep the code simple and the scoring brutal.

## License

MIT License - do whatever you want with this code.

## Disclaimer

This is just math applied to faces. Your worth as a human isn't determined by facial geometry ratios. I built this because the science is interesting, not to make anyone feel bad about their face.

Use for fun/education only.
# Eros
An Android Application built using flutter for front end and python and openCV for backend to analyze and give tips on facial features based on the distance, symmetry on facial landmarks and beauty standard of that region.