# 📚 Usage Examples & Code Snippets

Real-world examples of how to use the Face Recognition Movie Recommender system.

---

## 🚀 Quick Examples

### Example 1: Full Automated Flow

**Command:**
```bash
python app.py --flow
```

**What it does:**
1. Captures your face (20 samples)
2. Recognizes your face
3. Generates personalized recommendations
4. Asks if you want to rate movies

**Expected output:**
```
🚀 FULL FLOW: Capture → Recognize → Recommend
===============================================

Capture new face (c) or recognize existing (r)? (c/r): c

Enter person's name: Alex
Number of samples to capture (default 20): 20

📷 Starting face capture for: Alex
   [Camera opens, press 's' 20 times]
   ✓ Sample 1 captured
   ...
   ✓ Sample 20 captured

✅ Successfully registered Alex

✅ Working with: Alex

🎬 Generating personalized recommendations...

======================================================================
🎬 PERSONALIZED MOVIE RECOMMENDATIONS FOR: ALEX
======================================================================

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

======================================================================
```

---

## 💻 Programmatic Examples

### Example 2: Use in Your Own Python Script

```python
from model import FaceRecognitionModel
from recommender import MovieRecommender

# Initialize models
face_model = FaceRecognitionModel()
recommender = MovieRecommender()

# Step 1: Register a new face
print("Registering new face...")
success = face_model.capture_face_dataset("John", num_samples=20)

if success:
    # Step 2: Recognize the face
    recognized_name = face_model.recognize_faces_from_webcam(duration=10)
    
    if recognized_name:
        print(f"\n✅ Recognized: {recognized_name}")
        
        # Step 3: Get recommendations
        recommendations = recommender.get_recommendations(
            recognized_name, 
            top_n=4
        )
        
        # Step 4: Display recommendations
        recommender.display_recommendations(recognized_name, recommendations)
        
        # Step 5: Rate a movie
        if len(recommendations) > 0:
            top_movie = recommendations.iloc[0]
            recommender.rate_movie(recognized_name, top_movie["movie_id"], 9.0)
            print(f"✓ Rated '{top_movie['title']}': 9.0/10")
```

---

### Example 3: Batch Processing Multiple Users

```python
from model import FaceRecognitionModel
from recommender import MovieRecommender

face_model = FaceRecognitionModel()
recommender = MovieRecommender()

# Known users
users_to_process = ["Alice", "Bob", "Charlie"]

for user in users_to_process:
    print(f"\n🎬 Processing recommendations for {user}...")
    
    # Get recommendations
    recommendations = recommender.get_recommendations(user, top_n=4)
    
    # Display
    recommender.display_recommendations(user, recommendations)
    
    # Save to file
    output_file = f"recommendations_{user}.csv"
    recommendations.to_csv(output_file, index=False)
    print(f"✓ Saved to {output_file}")
```

---

### Example 4: Add User Ratings in Bulk

```python
from recommender import MovieRecommender

recommender = MovieRecommender()

# Define ratings for multiple users
users_ratings = {
    "Alice": {
        1: 9.0,    # The Shawshank Redemption: 9.0/10
        5: 8.5,    # Forrest Gump: 8.5/10
        8: 9.2,    # Interstellar: 9.2/10
    },
    "Bob": {
        2: 8.8,    # The Godfather: 8.8/10
        3: 9.0,    # The Dark Knight: 9.0/10
        6: 8.0,    # Inception: 8.0/10
    },
    "Charlie": {
        4: 7.5,    # Pulp Fiction: 7.5/10
        7: 8.6,    # Fight Club: 8.6/10
        15: 9.5,   # Se7en: 9.5/10
    }
}

# Process all ratings
for user, ratings in users_ratings.items():
    print(f"Rating movies for {user}...")
    for movie_id, rating in ratings.items():
        recommender.rate_movie(user, movie_id, rating)
        print(f"  ✓ Rated movie {movie_id}: {rating}/10")

print("\n✅ All ratings saved!")

# Now get recommendations for each user
for user in users_ratings.keys():
    recommendations = recommender.get_recommendations(user, top_n=4)
    recommender.display_recommendations(user, recommendations)
```

---

### Example 5: Export Recommendations as CSV

```python
from recommender import MovieRecommender
import pandas as pd

recommender = MovieRecommender()

# Get recommendations for multiple users
users = ["Alice", "Bob", "Charlie"]
all_recommendations = []

for user in users:
    recs = recommender.get_recommendations(user, top_n=4)
    recs["user"] = user
    all_recommendations.append(recs)

# Combine all recommendations
combined_df = pd.concat(all_recommendations, ignore_index=True)

# Save to CSV
combined_df.to_csv("all_recommendations.csv", index=False)

# Display statistics
print(f"\n📊 Exported {len(combined_df)} recommendations")
print(f"Users: {', '.join(combined_df['user'].unique())}")
```

---

### Example 6: Genre Analysis

```python
from recommender import MovieRecommender

recommender = MovieRecommender()

# Get movies by genre
genres = ["Sci-Fi", "Drama", "Action"]

for genre in genres:
    movies = recommender.get_movies_by_genre(genre)
    print(f"\n🎬 Top {genre} Movies:")
    print(f"{'Rank':<5} {'Title':<30} {'Year':<6} {'Rating':<8}")
    print("-" * 50)
    
    for idx, (_, movie) in enumerate(movies.head(5).iterrows(), 1):
        print(f"{idx:<5} {movie['title']:<30} {movie['year']:<6} {movie['rating']:<8}")
```

---

### Example 7: Custom Configuration

```python
from model import FaceRecognitionModel
from recommender import MovieRecommender
import config

# Adjust settings
config.FACE_RECOGNITION_TOLERANCE = 0.5  # Stricter matching
config.DEFAULT_FACE_SAMPLES = 30         # More samples
config.DEFAULT_RECOMMENDATIONS = 6       # More recommendations

# Now use models with custom config
face_model = FaceRecognitionModel()
recommender = MovieRecommender()

print(f"Tolerance: {config.FACE_RECOGNITION_TOLERANCE}")
print(f"Face Samples: {config.DEFAULT_FACE_SAMPLES}")
print(f"Recommendations: {config.DEFAULT_RECOMMENDATIONS}")
```

---

## 🎯 Real-World Scenarios

### Scenario A: Family Movie Night

```python
"""
Scenario: Help family members find movies to watch together
"""

from model import FaceRecognitionModel
from recommender import MovieRecommender

face_model = FaceRecognitionModel()
recommender = MovieRecommender()

# Get recommendations for each family member
family_members = face_model.get_known_faces()

print("\n🎬 Family Movie Night - Finding Common Interests")
print("=" * 60)

all_recommendations = {}

for member in family_members:
    recs = recommender.get_recommendations(member, top_n=4)
    all_recommendations[member] = set(recs['title'].tolist())
    
    print(f"\n{member}'s recommendations:")
    for movie in all_recommendations[member]:
        print(f"  • {movie}")

# Find movies that appeal to everyone
if len(family_members) > 1:
    common_movies = set.intersection(*all_recommendations.values())
    
    if common_movies:
        print("\n🌟 Movies Everyone Likes:")
        for movie in common_movies:
            print(f"  ✓ {movie}")
    else:
        print("\n⚠️ No movies appeal to everyone, but these are popular:")
        popular = recommender.movies_df.nlargest(3, 'rating')
        for _, movie in popular.iterrows():
            print(f"  • {movie['title']} ({movie['rating']}/10)")
```

---

### Scenario B: Recommendation System for Streaming App

```python
"""
Scenario: Integrate recommendations into a streaming platform
"""

from model import FaceRecognitionModel
from recommender import MovieRecommender
import json

face_model = FaceRecognitionModel()
recommender = MovieRecommender()

class StreamingApp:
    def __init__(self):
        self.face_model = face_model
        self.recommender = recommender
    
    def get_personalized_feed(self, user: str):
        """Get personalized movie feed for user"""
        recommendations = self.recommender.get_recommendations(user, top_n=4)
        
        feed = {
            "user": user,
            "recommendations": []
        }
        
        for _, movie in recommendations.iterrows():
            feed["recommendations"].append({
                "id": int(movie["movie_id"]),
                "title": movie["title"],
                "genre": movie["genre"],
                "rating": float(movie["rating"]),
                "year": int(movie["year"]),
                "watch_url": f"/watch/{movie['movie_id']}"
            })
        
        return feed
    
    def record_watch(self, user: str, movie_id: int, rating: float):
        """Record user watched and rated a movie"""
        self.recommender.rate_movie(user, movie_id, rating)
    
    def get_trending(self, genre: str = None):
        """Get trending movies"""
        if genre:
            movies = self.recommender.get_movies_by_genre(genre)
        else:
            movies = self.recommender.movies_df
        
        return movies.nlargest(5, "rating").to_dict("records")

# Usage
app = StreamingApp()

# Get personalized feed for Alice
feed = app.get_personalized_feed("Alice")
print(json.dumps(feed, indent=2))

# Record that Alice watched and rated a movie
app.record_watch("Alice", movie_id=1, rating=9.0)

# Get trending movies
trending = app.get_trending(genre="Sci-Fi")
print("\nTrending Sci-Fi Movies:")
for movie in trending:
    print(f"  • {movie['title']}: {movie['rating']}/10")
```

---

### Scenario C: Analyzing User Preferences

```python
"""
Scenario: Analyze what genres different users prefer
"""

from recommender import MovieRecommender
import pandas as pd

recommender = MovieRecommender()

# Sample ratings from different users
sample_ratings = {
    "Drama_Lover": {1: 9.0, 5: 8.8, 14: 9.2, 26: 8.5},  # High ratings for dramas
    "Action_Fan": {3: 9.0, 13: 8.8, 18: 8.5, 23: 8.2},   # Action movies
    "SciFi_Enthusiast": {6: 9.2, 8: 9.0, 9: 8.7, 30: 8.0},  # Sci-Fi movies
}

# Record all ratings
for user, ratings in sample_ratings.items():
    for movie_id, rating in ratings.items():
        recommender.rate_movie(user, movie_id, rating)

# Analyze preferences
print("\n📊 USER PREFERENCE ANALYSIS")
print("=" * 60)

for user in sample_ratings.keys():
    print(f"\n{user}:")
    
    # Get their ratings
    user_ratings = recommender.user_ratings.get(user, {})
    
    # Get the movies they rated
    rated_ids = [int(mid) for mid in user_ratings.keys()]
    rated_movies = recommender.movies_df[
        recommender.movies_df["movie_id"].isin(rated_ids)
    ]
    
    # Analyze genres
    genre_ratings = {}
    for _, movie in rated_movies.iterrows():
        genre = movie["genre"]
        rating = user_ratings[str(movie["movie_id"])]
        
        if genre not in genre_ratings:
            genre_ratings[genre] = []
        genre_ratings[genre].append(rating)
    
    # Display results
    sorted_genres = sorted(
        genre_ratings.items(),
        key=lambda x: sum(x[1])/len(x[1]),
        reverse=True
    )
    
    for genre, ratings in sorted_genres:
        avg_rating = sum(ratings) / len(ratings)
        print(f"  {genre}: {avg_rating:.1f}/10 (avg)")
```

---

## 📱 API Integration Example

### Example 8: Simple REST API

```python
"""
Create a simple REST API for recommendations
Requires: pip install flask
"""

from flask import Flask, jsonify, request
from model import FaceRecognitionModel
from recommender import MovieRecommender

app = Flask(__name__)
face_model = FaceRecognitionModel()
recommender = MovieRecommender()

@app.route('/api/recommendations/<user>', methods=['GET'])
def get_recommendations(user):
    """Get recommendations for a user"""
    try:
        recommendations = recommender.get_recommendations(user, top_n=4)
        
        return jsonify({
            "status": "success",
            "user": user,
            "recommendations": recommendations.to_dict("records")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/rate', methods=['POST'])
def rate_movie():
    """Rate a movie"""
    data = request.json
    user = data.get("user")
    movie_id = data.get("movie_id")
    rating = data.get("rating")
    
    if not all([user, movie_id, rating]):
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    
    try:
        recommender.rate_movie(user, movie_id, float(rating))
        return jsonify({"status": "success", "message": "Rating saved"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/movies/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    """Get movies by genre"""
    try:
        movies = recommender.get_movies_by_genre(genre)
        return jsonify({
            "status": "success",
            "genre": genre,
            "movies": movies.to_dict("records")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Usage:
# GET /api/recommendations/Alice
# POST /api/rate {"user": "Alice", "movie_id": 1, "rating": 9.0}
# GET /api/movies/Sci-Fi
```

---

## 🔧 Advanced Usage

### Example 9: Custom Recommendation Algorithm

```python
"""
Extend the recommender with custom algorithm
"""

from recommender import MovieRecommender
import numpy as np

class AdvancedRecommender(MovieRecommender):
    def get_recommendations_weighted(self, user: str, top_n: int = 4):
        """
        Advanced recommendations with custom weighting
        """
        user_preferences = self.user_ratings.get(user, {})
        
        if not user_preferences:
            return self._get_popular_recommendations(top_n)
        
        # Get rated movies
        rated_ids = [int(mid) for mid in user_preferences.keys()]
        rated_movies = self.movies_df[
            self.movies_df["movie_id"].isin(rated_ids)
        ].copy()
        
        # Get preferences
        genre_scores = {}
        avg_year = rated_movies["year"].mean()
        
        for _, movie in rated_movies.iterrows():
            genre = movie["genre"]
            rating = user_preferences[str(movie["movie_id"])]
            
            if genre not in genre_scores:
                genre_scores[genre] = []
            genre_scores[genre].append(rating)
        
        # Score unrated movies
        unrated = self.movies_df[
            ~self.movies_df["movie_id"].isin(rated_ids)
        ].copy()
        
        scores = []
        for _, movie in unrated.iterrows():
            genre_score = np.mean(genre_scores.get(movie["genre"], [0]))
            base_score = movie["rating"] / 10.0
            year_score = 1.0 if movie["year"] > avg_year else 0.8
            
            # Custom weighted formula
            combined = (
                genre_score * 0.4 +
                base_score * 0.4 +
                year_score * 0.2
            )
            scores.append(combined)
        
        unrated["score"] = scores
        return unrated.nlargest(top_n, "score")[
            ["movie_id", "title", "genre", "rating", "year"]
        ]

# Usage
rec = AdvancedRecommender()
rec.rate_movie("User1", 1, 9.0)
recommendations = rec.get_recommendations_weighted("User1", top_n=4)
print(recommendations)
```

---

## 📊 Data Analysis Example

### Example 10: Generate Recommendation Report

```python
"""
Generate a comprehensive recommendation report
"""

from recommender import MovieRecommender
import pandas as pd
from datetime import datetime

def generate_recommendation_report(users: list):
    """Generate detailed report for multiple users"""
    
    recommender = MovieRecommender()
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "users": {}
    }
    
    for user in users:
        recommendations = recommender.get_recommendations(user, top_n=4)
        user_ratings = recommender.user_ratings.get(user, {})
        
        report["users"][user] = {
            "total_ratings": len(user_ratings),
            "avg_rating": (
                sum(user_ratings.values()) / len(user_ratings)
                if user_ratings else 0
            ),
            "recommendations": recommendations.to_dict("records")
        }
    
    # Save report
    import json
    with open("recommendation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n📊 RECOMMENDATION REPORT")
    print("=" * 60)
    print(f"Generated: {report['generated_at']}")
    print(f"Users: {len(report['users'])}")
    
    for user, data in report["users"].items():
        print(f"\n{user}:")
        print(f"  Ratings: {data['total_ratings']}")
        print(f"  Avg Rating: {data['avg_rating']:.1f}/10")
        print(f"  Top Recommendation: {data['recommendations'][0]['title']}")

# Usage
users = ["Alice", "Bob", "Charlie"]
generate_recommendation_report(users)
```

---

## 🎓 Learning Resources in Code

All examples include:
- ✅ Clear comments explaining each step
- ✅ Error handling for robustness
- ✅ Real-world use cases
- ✅ Extensible patterns

**For more examples:**
- Check `README.md` for basic usage
- See `QUICKSTART.md` for quick reference
- Review `TROUBLESHOOTING.md` for common issues
- Examine code comments in `model.py`, `recommender.py`

---

*Happy coding and movie watching!* 🎬🍿
