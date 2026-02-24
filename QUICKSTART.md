# ⚡ Quick Start Guide

Get the Face Recognition Movie Recommender running in 5 minutes!

## 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

## 2. Run Setup (First Time Only)

```bash
python setup.py
```

This will:
- ✓ Verify Python 3.8+
- ✓ Check all dependencies
- ✓ Create data directories
- ✓ Initialize movie database

## 3. Choose Your Interface

### 🖥️ Terminal CLI (Recommended)

**Interactive menu:**
```bash
python app.py
```

**Full automated flow:**
```bash
python app.py --flow
```

### 🌐 Streamlit Web UI

```bash
streamlit run streamlit_app.py
```

## 4. First Run Steps

### Step 1: Register Your Face (30 seconds)
```
Menu > Option 1: Register New Face
- Enter your name
- Position yourself in front of camera
- Press 's' to capture 20 samples
- Press 'q' when done
```

### Step 2: Recognize Yourself (10 seconds)
```
Menu > Option 2: Recognize Face
- Look at camera for 10 seconds
- System identifies you
```

### Step 3: Get Recommendations (5 seconds)
```
Menu > Option 3: Get Recommendations
- Select your name
- View top 4 personalized movie suggestions
```

### Step 4: Rate Movies (Optional)
```
Menu > Option 4: Rate Movies
- Rate any movies 1-10
- Improves future recommendations
```

## 📁 Project Structure

```
face-movie-recommender/
├── app.py              # Main CLI application
├── model.py            # Face recognition
├── recommender.py      # Movie recommendations
├── streamlit_app.py    # Web UI
├── setup.py            # Setup script
├── requirements.txt    # Dependencies
├── README.md           # Full documentation
├── QUICKSTART.md       # This file
└── data/
    ├── movies.csv      # Movie dataset
    ├── user_ratings.json
    └── faces/
        └── face_encodings.pkl
```

## 🎯 Key Features

| Feature | What It Does |
|---------|-------------|
| **Register** | Capture your face from webcam (20+ samples) |
| **Recognize** | Identify yourself using face recognition |
| **Recommend** | Get personalized movie suggestions |
| **Rate** | Rate movies to improve recommendations |
| **Browse** | Explore movies by genre |

## 🐛 Quick Troubleshooting

### "Could not open webcam"
```bash
# Test if webcam works
python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam OK' if cap.isOpened() else 'Webcam FAILED')"
```
- Close other apps using camera
- Check camera permissions

### "face_recognition not found"
```bash
# May take 5-10 minutes to compile
pip install --no-cache-dir face_recognition
```

### "No face detected"
- ✓ Ensure good lighting
- ✓ Face 2-3 feet from camera
- ✓ Face fully visible (not tilted >45°)
- ✓ Try different angles

### "Low recognition accuracy"
- Capture more samples (30-50)
- Use varied lighting and angles
- Remove glasses/hats during capture

## 🎬 Example Workflow

```bash
# Terminal 1: Start the app
$ python app.py

===============================================
    🎬 FACE RECOGNITION MOVIE RECOMMENDER 🎬
===============================================

📋 MAIN MENU
1. Register New Face
2. Recognize Face
3. Get Movie Recommendations
4. Rate Movie
5. View All Known Faces
6. View Movies by Genre
7. Exit

# Input: 1 (Register New Face)
Enter person's name: Alex
Number of samples to capture (default 20): 20

📷 Starting face capture for: Alex
   Capturing 20 samples. Look at the camera from different angles.
   Press 'q' to quit, 's' to capture sample

   [Camera opens, press 's' 20 times]
   ✓ Sample 1 captured
   ✓ Sample 2 captured
   ...
   ✓ Sample 20 captured

✅ Successfully added 20 samples for Alex

# Input: 2 (Recognize Face)
👁️ Starting face recognition for 10 seconds...
   Looking for known faces...

   [Look at camera]
   
✅ Recognized: Alex

# Input: 3 (Get Recommendations)
Select person: 1. Alex
Select person (number or name): 1

🍿 PERSONALIZED MOVIE RECOMMENDATIONS FOR: ALEX
======================================================

1. Inception (2010)
   Genre: Sci-Fi
   Rating: 8.8/10

2. The Matrix (1999)
   Genre: Sci-Fi
   Rating: 8.7/10

3. Interstellar (2014)
   Genre: Sci-Fi
   Rating: 8.7/10

4. Dune (2021)
   Genre: Sci-Fi
   Rating: 8.0/10

Would you like to rate any of these movies? (y/n): y
```

## 🚀 Advanced Usage

### Full Automated Flow
```bash
python app.py --flow
```
This runs: Register → Recognize → Get Recommendations in one go

### Use Specific Data Directory
```python
from model import FaceRecognitionModel
model = FaceRecognitionModel(data_dir="my_faces")
```

### Custom Movie Database
Edit `recommender.py` and add movies to the dataset, then:
```bash
python -c "from recommender import MovieRecommender; MovieRecommender().load_data()"
```

### Rate Movies in Bulk
```python
from recommender import MovieRecommender

rec = MovieRecommender()
rec.rate_movie("Alex", movie_id=1, rating=9.0)
rec.rate_movie("Alex", movie_id=5, rating=8.5)
rec.rate_movie("Alex", movie_id=10, rating=7.0)
```

## 📊 How Recommendations Work

1. **New Users**: Get top-rated movies
2. **Returning Users**: 
   - System learns your genre preferences
   - Scores unrated movies based on:
     - Similar genres to ones you rated well
     - Movie quality (base rating)
     - Recency (newer movies get slight boost)
   - Shows top 4 recommendations

## 🎓 Learning More

- **Full Documentation**: See `README.md`
- **Code**: Check inline comments in `model.py`, `recommender.py`, `app.py`
- **Face Recognition**: https://github.com/ageitgey/face_recognition
- **OpenCV**: https://docs.opencv.org/

## 💡 Tips for Best Results

✅ **Face Registration**
- Good lighting (natural light best)
- Different angles and distances
- Various facial expressions
- 20-50 samples recommended

✅ **Face Recognition**
- Same lighting as registration
- Face clearly visible
- Similar distance as registration
- No extreme tilting

✅ **Recommendations**
- Rate a few movies first
- Rate diverse genres
- Update ratings as tastes change
- System improves with more data

## 🎬 Next Steps

1. **Run it**: `python app.py --flow`
2. **Explore**: Try different features
3. **Customize**: Edit movie database in `recommender.py`
4. **Enhance**: Add more face samples for accuracy
5. **Share**: Show friends and get them recognized!

---

**Questions?** See the full `README.md` or check code comments for detailed explanations.

**Happy watching!** 🍿🎬
