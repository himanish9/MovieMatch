# 🔧 Troubleshooting Guide

Solutions for common issues with the Face Recognition Movie Recommender.

---

## 🎥 Webcam Issues

### Issue: "Could not open webcam"

**Error Message:**
```
❌ Error: Could not open webcam
```

**Solutions:**

1. **Check if webcam is available:**
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam works!' if cap.isOpened() else 'Webcam failed')"
   ```

2. **Try different camera indices:**
   ```python
   # Edit model.py and change CAMERA_INDEX
   for i in range(5):
       cap = cv2.VideoCapture(i)
       if cap.isOpened():
           print(f"Webcam found at index {i}")
   ```

3. **On Linux - Give camera permissions:**
   ```bash
   sudo usermod -aG video $USER
   sudo reboot  # Logout and login
   ```

4. **On macOS - Grant camera access:**
   - System Preferences → Security & Privacy → Camera
   - Allow Terminal/Python to access camera

5. **On Windows - Check Device Manager:**
   - Device Manager → Cameras
   - Ensure camera is not disabled
   - Right-click → Enable if needed

6. **Close conflicting applications:**
   - Close Zoom, Skype, Teams, etc.
   - These may lock the webcam

7. **Try a different USB port:**
   - If using external webcam, try different USB port

---

## 👁️ Face Recognition Issues

### Issue: "No face detected"

**Causes & Solutions:**

1. **Poor lighting:**
   ```
   ✅ DO: Use natural light or bright room
   ❌ DON'T: Use dim lighting or backlight
   ```

2. **Face not fully visible:**
   ```
   ✅ DO: Position face centrally in frame
   ❌ DON'T: Tilt head >45°, partially hide face
   ```

3. **Distance from camera:**
   ```
   ✅ DO: Position 2-3 feet from camera
   ❌ DON'T: Too close (<1 ft) or too far (>5 ft)
   ```

4. **Obstacles:**
   ```
   ✅ DO: Remove glasses, hats, masks if possible
   ❌ DON'T: Wear excessive face coverings
   ```

5. **Test face detection alone:**
   ```python
   import cv2
   from model import FaceRecognitionModel
   
   model = FaceRecognitionModel()
   # Run recognition - if it still fails, the library has issues
   ```

### Issue: Low recognition accuracy / "Unknown" faces

**Causes & Solutions:**

1. **Not enough training samples:**
   - Increase from 20 to 30-50 samples
   - Run registration again: Select option 1

2. **Inconsistent conditions during training:**
   ```
   ✅ DO: Capture from multiple angles, distances, lighting
   ❌ DON'T: All samples from same angle
   ```

3. **Adjust recognition tolerance:**
   ```python
   # Edit model.py, line ~145:
   matches = face_recognition.compare_faces(
       self.known_face_encodings,
       face_encoding,
       tolerance=0.5  # Lower = stricter (try 0.5-0.7)
   )
   ```

4. **Check encoding quality:**
   ```python
   from model import FaceRecognitionModel
   model = FaceRecognitionModel()
   print(f"Known faces: {len(model.known_face_encodings)}")
   print(f"Known names: {model.known_face_names}")
   ```

5. **Re-register with better samples:**
   - Delete old recordings
   - Rerun registration with 50 samples
   - Use varied conditions

### Issue: "Recognized: Unknown"

**Causes:**
- Face matches no known person
- Recognition confidence too low

**Solutions:**
1. Register more faces
2. Lower tolerance (more lenient)
3. Use better lighting and distance

---

## 📦 Installation Issues

### Issue: "face_recognition module not found"

**Solutions:**

1. **Install with no cache:**
   ```bash
   pip install --no-cache-dir face-recognition
   ```
   This takes 5-10 minutes as it compiles dlib.

2. **Check if dlib installed:**
   ```bash
   pip list | grep dlib
   ```

3. **On macOS with Apple Silicon:**
   ```bash
   # May need conda instead
   conda install face-recognition
   ```

4. **On Windows with errors:**
   ```bash
   # Install Visual C++ Build Tools first
   # Then: pip install --no-cache-dir face-recognition
   ```

### Issue: "OpenCV import failed"

**Error:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solution:**
```bash
pip install opencv-python
# Or with no cache:
pip install --no-cache-dir opencv-python
```

### Issue: "scikit-learn version mismatch"

**Error:**
```
sklearn version conflict
```

**Solution:**
```bash
pip install --upgrade scikit-learn pandas numpy
```

### Issue: "Pillow import error"

**Solution:**
```bash
pip install Pillow
# Or for Streamlit UI:
pip install streamlit
```

---

## 🎬 Movie Recommendation Issues

### Issue: "No recommendations available"

**Causes & Solutions:**

1. **No user rating history:**
   - Rate some movies first (Option 4)
   - System needs at least 1 rating to personalize

2. **All movies already rated:**
   - System has no new movies to recommend
   - Add more movies to `data/movies.csv`

3. **Rating file corrupted:**
   ```bash
   rm data/user_ratings.json
   # System will create new one
   ```

4. **Check rating format:**
   ```python
   import json
   with open("data/user_ratings.json", "r") as f:
       data = json.load(f)
       print(data)
   ```

### Issue: "Movies CSV not found"

**Error:**
```
⚠️ Movies CSV not found. Creating sample dataset...
```

**This is expected** - system creates sample dataset automatically.

To use custom movies:
1. Create `data/movies.csv` with columns: movie_id, title, genre, rating, year
2. Or edit `recommender.py` to load from different source

### Issue: Same recommendations for all users

**Cause:** Users have no rating history

**Solution:**
1. Each user must rate some movies first
2. Ratings create personalization
3. Without ratings, system shows top-rated movies (which is correct behavior)

---

## 💾 Storage Issues

### Issue: "Face encodings file corrupted"

**Error:**
```
EOFError: pickle data was truncated
```

**Solution:**
```bash
# Remove corrupted file
rm data/faces/face_encodings.pkl
# Re-register faces
python app.py  # Option 1: Register New Face
```

### Issue: "Permission denied" when saving

**On Linux/macOS:**
```bash
chmod 755 data/
chmod 755 data/faces/
```

**On Windows:**
- Right-click data folder → Properties
- Uncheck "Read-only"
- Apply to all files

### Issue: Disk space problems

**Check space:**
```bash
du -sh data/  # Linux/macOS
dir /s data   # Windows
```

**Solution:**
- Face encodings: ~1-2MB per 20 faces
- Ratings: ~1KB per user
- Movies: <1MB
- Total: Negligible for typical use

---

## 🖥️ Application Issues

### Issue: App crashes after face capture

**Error:**
```
Exception in face recognition...
```

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Check memory:**
   ```bash
   # Linux/macOS:
   free -h
   # Windows:
   tasklist /v | find "python"
   ```

3. **Check if face encoding failed:**
   ```python
   from model import FaceRecognitionModel
   model = FaceRecognitionModel()
   print(f"Encodings: {len(model.known_face_encodings)}")
   ```

4. **Run with debug output:**
   ```python
   # Edit app.py, enable logging:
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### Issue: Slow performance

**Causes:**

1. **High resolution video:**
   - Edit `model.py` line ~60:
   ```python
   small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Reduce to 0.15
   ```

2. **Processing every frame:**
   - Edit `config.py`:
   ```python
   FRAME_SKIP = 2  # Process every 2nd frame
   ```

3. **Many faces in database:**
   - Recognition gets slower with >100 faces
   - Consider splitting into groups

4. **Recommendations calculation:**
   - Disable Streamlit for faster CLI
   - Reduce movie database size

### Issue: Terminal UI not displaying correctly

**Solutions:**

1. **Clear terminal:**
   ```bash
   clear   # Linux/macOS
   cls     # Windows
   ```

2. **Check terminal size:**
   ```bash
   # Resize terminal to larger size
   ```

3. **Disable emojis:**
   - Edit `app.py` and remove emoji characters
   - Or set `DEBUG_MODE = False` in `config.py`

4. **Use simpler interface:**
   ```bash
   # Use plain Python output
   python app.py 2>/dev/null
   ```

---

## 🌐 Streamlit UI Issues

### Issue: "Streamlit not installed"

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install streamlit
```

### Issue: "Port already in use"

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Use different port:
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Webcam not working in Streamlit

**Note:** Real-time webcam in Streamlit requires different approach.

**Workaround:**
- Use terminal CLI for webcam features: `python app.py`
- Use Streamlit for browsing and rating only

---

## 🔍 Debugging Steps

### General Debugging Checklist

1. **Check Python version:**
   ```bash
   python --version
   ```

2. **Verify all dependencies:**
   ```bash
   python -c "import cv2, face_recognition, pandas, sklearn; print('OK')"
   ```

3. **Run setup validation:**
   ```bash
   python setup.py
   ```

4. **Check data files:**
   ```bash
   ls -la data/  # Linux/macOS
   dir data      # Windows
   ```

5. **Test individual components:**
   ```python
   # Test face recognition
   python -c "from model import FaceRecognitionModel; m = FaceRecognitionModel(); print('✓ Face model OK')"
   
   # Test recommender
   python -c "from recommender import MovieRecommender; r = MovieRecommender(); print('✓ Recommender OK')"
   ```

6. **Run with debug mode:**
   ```python
   # Edit config.py:
   DEBUG_MODE = True
   ```

### Enable Verbose Output

```python
# Add to app.py after imports:
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s'
)
```

---

## 📋 Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Could not open webcam` | Camera not available | Check camera, close other apps |
| `No faces detected` | Poor lighting/angle | Improve lighting, position face |
| `face_recognition not found` | Not installed | `pip install face_recognition` |
| `pickle data was truncated` | Corrupted file | Delete `data/faces/face_encodings.pkl` |
| `No module named 'cv2'` | OpenCV not installed | `pip install opencv-python` |
| `Address already in use` | Port occupied | Use different port for Streamlit |

---

## 🆘 Getting More Help

1. **Check existing issues:** Search GitHub/forums for error message
2. **Read documentation:** See `README.md` for detailed info
3. **Test individual modules:**
   ```bash
   python -c "from model import FaceRecognitionModel; ..."
   ```
4. **Look at code comments:** All files have detailed docstrings
5. **Check config.py:** Many settings are customizable

---

## 💡 Pro Tips

1. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Save debug output to file:**
   ```bash
   python app.py > debug.log 2>&1
   ```

3. **Test with sample data:**
   ```bash
   python -c "from recommender import MovieRecommender; r = MovieRecommender(); print(r.movies_df.head())"
   ```

4. **Monitor performance:**
   ```bash
   # Linux/macOS:
   time python app.py --flow
   ```

5. **Clear cache if issues persist:**
   ```bash
   rm -rf data/faces/
   rm data/user_ratings.json
   rm data/movies.csv
   python setup.py  # Reinitialize
   ```

---

## 🎯 If All Else Fails

1. **Clean reinstall:**
   ```bash
   rm -rf venv/
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python setup.py
   ```

2. **Try from scratch:**
   - Delete all `data/` contents
   - Rerun `python setup.py`
   - Start fresh: `python app.py --flow`

3. **Test basic functionality:**
   ```bash
   python -c "
   from model import FaceRecognitionModel
   from recommender import MovieRecommender
   print('✓ Models import successfully')
   m = FaceRecognitionModel()
   r = MovieRecommender()
   print('✓ Models initialize successfully')
   print('✓ All systems ready!')
   "
   ```

---

**Still having issues?** Review the relevant section above or check `README.md` for comprehensive documentation.

*Remember: Most issues are environment-related, not code-related!* 🎬
