# Emotion-Based Movie Recommendation System Update

## Overview
The system now detects facial emotions (happy, angry, neutral) and provides personalized movie recommendations based on detected emotion and the new movie database.

## Changes Made

### 1. Movie Database Updated (`recommender.py`)
**New Movies Added:**
- **Funny Movies (10):** Mathu Vadalara 2, Aay, Maruthi Nagar Subramanyam, 35 Chinna Katha Kaadu, MAD, Janaka Aithe Ganaka, Premante, Mithra Mandali, Subham, The Great Pre-Wedding Show
- **Horror Movies (10):** Kishkindhapuri, Ghatikachalam, Jatadhara, Odela 2, Chandramukhi 2, Bhoo, Karthikeya 2, Stree 2, Bhediya, Tumbbad
- **Action Movies (10):** Akhanda, Krack, Saaho, Pushpa: The Rise, RRR, Bhairava, Kalki 2898 AD, Master, Beast, Khel Khel Mein
- **Romance Movies (10):** Kabali, Prem Amar Bondhu, Love Story, Raees, Drishyam, Arjun Reddy, Majnu, Lovers, Romance, Sweetheart

**Total: 40 movies with ratings and release years**

### 2. Emotion Detection Engine (`model.py`)
**New Methods Added:**

#### `detect_emotion(frame) -> str`
- Analyzes facial landmarks using OpenCV and face_recognition
- Detects mouth shape and eye openness
- Returns: 'happy', 'angry', or 'neutral'
- Uses corner detection and brightness analysis for accuracy

#### `recognize_with_emotion(duration) -> Tuple[Optional[str], str]`
- Simultaneous face recognition and emotion detection
- Returns recognized name and detected emotion
- Displays emotion labels on video frames

### 3. Emotion-Based Recommendations (`recommender.py`)
**New Method:**

#### `get_emotion_based_recommendations(emotion, top_n=4) -> DataFrame`
**Recommendation Logic:**
- **Happy/Laughing:** Horror, Action & Romance movies
- **Angry:** Comedy, Action & Romance movies
- **Neutral:** Movies from all categories (Comedy, Horror, Action, Romance)

### 4. Frontend Updates

#### `face-capture-section.tsx`
- Added emotion detection during face capture
- Uses canvas analysis to detect mouth brightness
- Tracks emotion across 20 frames and selects most common
- Passes detected emotion to next stage

#### `recommendations-section.tsx`
- Receives detected emotion as prop
- Displays emotion badge with explanation
- Shows which categories are being recommended based on emotion

#### `app/page.tsx`
- Added emotion state management
- Passes emotion through component chain
- Resets emotion on restart

### 5. API Endpoint (`app/api/recommendations/route.ts`)
- Updated to accept `emotion` parameter
- Updated movie database with all 40 new movies
- Implements emotion-based filtering logic
- Returns top 4 movies matching emotion criteria

## Recommendation Rules

```
IF face shows HAPPY/LAUGHING expression:
  ↓
  Recommend: Horror, Action, Romance movies
  😊 "Detected Happy Expression! Recommending Horror, Action & Love movies..."

IF face shows ANGRY expression:
  ↓
  Recommend: Comedy, Action, Romance movies
  😠 "Detected Angry Expression! Recommending Funny, Action & Love movies..."

IF face shows NEUTRAL expression:
  ↓
  Recommend: All categories (Comedy, Horror, Action, Romance)
  😐 "Detected Neutral Expression! Recommending movies from all categories..."
```

## How It Works (Step-by-Step)

1. **User enters name** → Stage: Name Input
2. **User captures face** → Stage: Face Capture
   - 20 frames analyzed for emotion
   - Mouth brightness analyzed using canvas
   - Most common emotion detected
3. **Emotion passed to recommendations** → Stage: Recommendations
   - API receives emotion parameter
   - Filters movies by emotion-matched genres
   - Displays top 4 by rating
4. **Results displayed** with:
   - Emotion indicator
   - Recommended movie titles
   - Genres and ratings
   - Release years

## Emotion Detection Algorithm

### Brightness Analysis
- Analyzes mouth region (lower 25% of face, middle 60% of width)
- Counts bright pixels (brightness > 150)
- Calculates bright ratio:
  - **Ratio > 0.5** = Happy (mouth open, smile visible)
  - **Ratio < 0.2** = Angry (closed mouth, narrow lips)
  - **Ratio 0.2-0.5** = Neutral (relaxed expression)

### Accuracy Notes
- Works best in well-lit environments
- Detects natural expressions during face capture
- Averaged across multiple frames for stability
- Combines with facial landmarks for better accuracy

## Technical Details

### Dependencies
- `cv2` (OpenCV) - Image processing
- `face_recognition` - Facial analysis
- Canvas API - Browser-side image processing
- NumPy - Numerical operations

### File Changes
- `recommender.py` - Movie data + emotion method
- `model.py` - Emotion detection + recognition
- `face-capture-section.tsx` - Canvas emotion detection
- `recommendations-section.tsx` - Emotion display
- `app/page.tsx` - Emotion state management
- `app/api/recommendations/route.ts` - Emotion-based API

## Testing the Feature

1. Run the web application
2. Enter your name
3. Click "Capture Face"
4. **Try different expressions:**
   - Smile/laugh → Get Horror, Action, Romance movies
   - Angry/frown → Get Comedy, Action, Romance movies
   - Neutral/calm → Get movies from all categories
5. View personalized recommendations

## Future Enhancements

- Multi-emotion detection across time (mood trends)
- Emotion confidence scores
- User preference override options
- Emotion-based watchlist generation
- Historical emotion tracking
- Micro-expression detection for subtle emotions

---

**Update Version:** 2.0
**Last Updated:** 2026-02-24
**Status:** Ready for Production
