"""
Movie Recommendation System
Uses collaborative filtering with scikit-learn
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import json


class MovieRecommender:
    def __init__(self, movies_csv: str = "data/movies.csv"):
        self.movies_csv = Path(movies_csv)
        self.user_ratings = {}
        self.load_data()
        self.ratings_file = Path("data/user_ratings.json")
        self.load_user_ratings()

    def load_data(self):
        """Load movies dataset"""
        if not self.movies_csv.exists():
            print("⚠️ Movies CSV not found. Creating sample dataset...")
            self.create_sample_dataset()

        self.movies_df = pd.read_csv(self.movies_csv)
        print(f"✓ Loaded {len(self.movies_df)} movies")

    def create_sample_dataset(self):
        """Create a sample movies dataset with realistic data"""
        movies_data = {
            "movie_id": range(1, 41),
            "title": [
                # Funny Movies (10)
                "Mathu Vadalara 2",
                "Aay",
                "Maruthi Nagar Subramanyam",
                "35 Chinna Katha Kaadu",
                "MAD",
                "Janaka Aithe Ganaka",
                "Premante",
                "Mithra Mandali",
                "Subham",
                "The Great Pre-Wedding Show",
                # Horror Movies (10)
                "Kishkindhapuri",
                "Ghatikachalam",
                "Jatadhara",
                "Odela 2",
                "Chandramukhi 2",
                "Bhoo",
                "Karthikeya 2",
                "Stree 2",
                "Bhediya",
                "Tumbbad",
                # Action Movies (10)
                "Akhanda",
                "Krack",
                "Saaho",
                "Pushpa: The Rise",
                "RRR",
                "Bhairava",
                "Kalki 2898 AD",
                "Master",
                "Beast",
                "Khel Khel Mein",
                # Love/Romance Movies (10)
                "Kabali",
                "Prem Amar Bondhu",
                "Love Story",
                "Raees",
                "Drishyam",
                "Arjun Reddy",
                "Majnu",
                "Lovers",
                "Romance",
                "Sweetheart",
            ],
            "genre": [
                # Funny
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                "Comedy",
                # Horror
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                "Horror",
                # Action
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                "Action",
                # Love
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
                "Romance",
            ],
            "rating": [
                # Funny
                8.2, 7.5, 7.2, 7.8, 7.3, 6.5, 6.2, 2.5, 7.2, 7.0,
                # Horror
                6.9, 6.1, 3.3, 4.6, 7.4, 6.8, 7.1, 7.3, 7.0, 7.5,
                # Action
                8.5, 8.3, 7.9, 8.1, 9.0, 8.0, 8.4, 8.2, 7.8, 7.6,
                # Love
                8.0, 7.8, 7.5, 8.1, 8.3, 8.2, 7.9, 7.7, 7.4, 7.6,
            ],
            "year": [
                # Funny
                2024, 2024, 2024, 2024, 2023, 2024, 2025, 2025, 2025, 2025,
                # Horror
                2025, 2025, 2025, 2025, 2024, 2024, 2023, 2024, 2023, 2022,
                # Action
                2024, 2023, 2019, 2021, 2022, 2024, 2023, 2019, 2024, 2021,
                # Love
                2015, 2020, 2021, 2014, 2015, 2017, 2013, 2016, 2018, 2019,
            ],
        }

        df = pd.DataFrame(movies_data)
        self.movies_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.movies_csv, index=False)
        print(f"✓ Created sample dataset with {len(df)} movies")
        self.movies_df = df

    def load_user_ratings(self):
        """Load user rating history"""
        if self.ratings_file.exists():
            with open(self.ratings_file, "r") as f:
                self.user_ratings = json.load(f)
        else:
            self.user_ratings = {}

    def save_user_ratings(self):
        """Save user rating history"""
        self.ratings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ratings_file, "w") as f:
            json.dump(self.user_ratings, f, indent=2)

    def rate_movie(self, user: str, movie_id: int, rating: float):
        """Record a user's rating for a movie"""
        if user not in self.user_ratings:
            self.user_ratings[user] = {}
        self.user_ratings[user][str(movie_id)] = rating
        self.save_user_ratings()

    def get_recommendations(self, user: str, top_n: int = 4) -> pd.DataFrame:
        """
        Get personalized movie recommendations using content-based filtering
        combined with user preferences
        
        Args:
            user: Username
            top_n: Number of recommendations to return
            
        Returns:
            DataFrame with top N recommended movies
        """
        # Get user's rating history
        user_preferences = self.user_ratings.get(user, {})

        if not user_preferences:
            # If user has no history, recommend popular movies
            print(f"ℹ No rating history for {user}. Recommending popular movies...")
            return self._get_popular_recommendations(top_n)

        # Get rated movies
        rated_ids = [int(mid) for mid in user_preferences.keys()]
        rated_movies = self.movies_df[
            self.movies_df["movie_id"].isin(rated_ids)
        ].copy()

        # Calculate genre preferences based on ratings
        genre_scores = {}
        for _, movie in rated_movies.iterrows():
            movie_id = movie["movie_id"]
            rating = user_preferences[str(movie_id)]
            genre = movie["genre"]

            if genre not in genre_scores:
                genre_scores[genre] = []
            genre_scores[genre].append(rating)

        # Calculate average rating per genre
        avg_genre_ratings = {
            genre: np.mean(ratings) for genre, ratings in genre_scores.items()
        }

        # Score unrated movies based on similarity
        unrated_movies = self.movies_df[
            ~self.movies_df["movie_id"].isin(rated_ids)
        ].copy()

        scores = []
        for _, movie in unrated_movies.iterrows():
            # Combine factors: genre preference, base rating, recency
            genre_score = avg_genre_ratings.get(movie["genre"], 0)
            base_score = movie["rating"] / 10.0
            recency_boost = (2024 - movie["year"]) / 100.0  # Recent movies get bonus

            combined_score = (
                genre_score * 0.5 + base_score * 0.35 + recency_boost * 0.15
            )
            scores.append(combined_score)

        unrated_movies["recommendation_score"] = scores

        # Get top recommendations
        recommendations = unrated_movies.nlargest(
            top_n, "recommendation_score"
        )[["movie_id", "title", "genre", "rating", "year"]]

        return recommendations.reset_index(drop=True)

    def _get_popular_recommendations(self, top_n: int = 4) -> pd.DataFrame:
        """Get top-rated movies as recommendations"""
        return self.movies_df.nlargest(top_n, "rating")[
            ["movie_id", "title", "genre", "rating", "year"]
        ].reset_index(drop=True)

    def display_recommendations(
        self, user: str, recommendations: pd.DataFrame
    ):
        """Pretty print movie recommendations"""
        print("\n" + "=" * 70)
        print(f"🎬 PERSONALIZED MOVIE RECOMMENDATIONS FOR: {user.upper()}")
        print("=" * 70)

        if recommendations.empty:
            print("No recommendations available.")
            return

        for idx, (_, movie) in enumerate(recommendations.iterrows(), 1):
            print(
                f"\n{idx}. {movie['title']} ({movie['year']})"
            )
            print(f"   Genre: {movie['genre']}")
            print(f"   Rating: {movie['rating']:.1f}/10")

        print("\n" + "=" * 70)

    def get_movies_by_genre(self, genre: str) -> pd.DataFrame:
        """Get movies of a specific genre"""
        return self.movies_df[self.movies_df["genre"] == genre].sort_values(
            "rating", ascending=False
        )

    def get_emotion_based_recommendations(self, emotion: str, top_n: int = 4) -> pd.DataFrame:
        """
        Get movie recommendations based on detected emotion
        
        Args:
            emotion: Detected emotion ('happy', 'angry', 'neutral')
            top_n: Number of recommendations to return
            
        Returns:
            DataFrame with top N recommended movies for the emotion
        """
        emotion = emotion.lower().strip()
        
        if emotion in ['happy', 'laughing']:
            # Happy/Laughing: Horror, Action, Love
            genres = ['Horror', 'Action', 'Romance']
            print(f"😊 Detected Happy Expression! Recommending Horror, Action & Love movies...")
        elif emotion == 'angry':
            # Angry: Funny, Action, Love
            genres = ['Comedy', 'Action', 'Romance']
            print(f"😠 Detected Angry Expression! Recommending Funny, Action & Love movies...")
        elif emotion == 'neutral':
            # Neutral: All categories
            genres = ['Comedy', 'Horror', 'Action', 'Romance']
            print(f"😐 Detected Neutral Expression! Recommending movies from all categories...")
        else:
            # Default to all categories
            genres = ['Comedy', 'Horror', 'Action', 'Romance']
            print(f"ℹ Unknown emotion '{emotion}'. Recommending popular movies from all categories...")
        
        # Filter movies by selected genres
        filtered_movies = self.movies_df[self.movies_df['genre'].isin(genres)]
        
        # Get top N by rating
        recommendations = filtered_movies.nlargest(top_n, 'rating')[
            ['movie_id', 'title', 'genre', 'rating', 'year']
        ].reset_index(drop=True)
        
        return recommendations
