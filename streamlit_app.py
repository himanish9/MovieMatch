"""
Streamlit Web UI for Face Recognition Movie Recommender
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from model import FaceRecognitionModel
from recommender import MovieRecommender
import tempfile
import os


# Page config
st.set_page_config(
    page_title="🎬 Face Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "face_model" not in st.session_state:
    st.session_state.face_model = FaceRecognitionModel()

if "recommender" not in st.session_state:
    st.session_state.recommender = MovieRecommender()

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .recommendation-score {
        font-size: 18px;
        color: #FFB703;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    st.markdown(
        "<h1 class='main-header'>🎬 Face Recognition Movie Recommender 🎬</h1>",
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    with st.sidebar:
        st.title("📋 Menu")
        page = st.radio(
            "Select an option:",
            [
                "🏠 Home",
                "📝 Register Face",
                "👁️ Recognize Face",
                "🍿 Get Recommendations",
                "⭐ Rate Movies",
                "👥 Known Faces",
                "🎬 Browse Movies",
            ],
        )

    # Home page
    if page == "🏠 Home":
        show_home()

    # Register Face
    elif page == "📝 Register Face":
        show_register_face()

    # Recognize Face
    elif page == "👁️ Recognize Face":
        show_recognize_face()

    # Get Recommendations
    elif page == "🍿 Get Recommendations":
        show_get_recommendations()

    # Rate Movies
    elif page == "⭐ Rate Movies":
        show_rate_movies()

    # Known Faces
    elif page == "👥 Known Faces":
        show_known_faces()

    # Browse Movies
    elif page == "🎬 Browse Movies":
        show_browse_movies()


def show_home():
    st.markdown("## Welcome! 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        ### 🎯 What This App Does
        
        This intelligent system combines:
        
        - **👁️ Face Recognition** - Identify people from webcam
        - **🎬 Movie Recommendations** - Personalized recommendations using ML
        - **⭐ Rating System** - Improve recommendations by rating movies
        
        ### 🚀 Quick Start
        
        1. **Register** your face in the database
        2. **Recognize** yourself using the webcam
        3. **Get** personalized movie recommendations
        4. **Rate** movies to improve future suggestions
        """
        )

    with col2:
        st.markdown(
            """
        ### 📊 Features
        
        ✅ **Automatic Dataset Creation** - Build face database on-the-fly
        
        ✅ **Smart Recommendations** - Uses collaborative & content filtering
        
        ✅ **Genre Browsing** - Explore movies by category
        
        ✅ **Rating History** - Track your preferences over time
        
        ✅ **Multi-User** - Supports multiple recognized people
        """
        )

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Known Faces", len(st.session_state.face_model.get_known_faces()))
    with col2:
        st.metric(
            "Movies Available", len(st.session_state.recommender.movies_df)
        )
    with col3:
        genres = st.session_state.recommender.movies_df["genre"].nunique()
        st.metric("Genres", genres)


def show_register_face():
    st.markdown("## 📝 Register New Face")

    name = st.text_input("Enter person's name:").strip()

    if not name:
        st.info("Please enter a name to register")
        return

    num_samples = st.number_input(
        "Number of face samples to capture:", min_value=5, max_value=50, value=20
    )

    if st.button("🎥 Start Face Capture", key="register_btn"):
        with st.spinner(f"Capturing {num_samples} samples for {name}..."):
            # Note: In Streamlit, real-time webcam capture requires a different approach
            st.info(
                """
                For real-time webcam capture, use the **Terminal CLI**:
                ```bash
                python app.py
                ```
                Then select option 1 to register a new face.
                
                Or run the full flow:
                ```bash
                python app.py --flow
                ```
                """
            )


def show_recognize_face():
    st.markdown("## 👁️ Recognize Face")

    known_faces = st.session_state.face_model.get_known_faces()

    if not known_faces:
        st.error("❌ No known faces in database. Register faces first!")
        return

    st.info(
        """
        For real-time face recognition from webcam, use the **Terminal CLI**:
        ```bash
        python app.py
        ```
        Then select option 2 to recognize faces.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Or select manually:")
        selected = st.selectbox("Choose a person:", known_faces)
        if st.button("✓ Select this person"):
            st.session_state.current_user = selected
            st.success(f"Selected: {selected}")

    with col2:
        st.subheader("Quick Stats")
        for face in known_faces:
            count = st.session_state.face_model.known_face_names.count(face)
            st.text(f"{face}: {count} samples")


def show_get_recommendations():
    st.markdown("## 🍿 Get Recommendations")

    known_faces = st.session_state.face_model.get_known_faces()

    if not known_faces:
        st.error("❌ No known faces in database. Register faces first!")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        person = st.selectbox("Select person:", known_faces)

    with col2:
        if st.button("Get Recommendations"):
            st.session_state.current_user = person

    if st.session_state.current_user:
        person = st.session_state.current_user
        st.subheader(f"🎬 Recommendations for {person}")

        recommendations = st.session_state.recommender.get_recommendations(
            person, top_n=4
        )

        if recommendations.empty:
            st.info("No recommendations yet. Rate some movies first!")
        else:
            # Display recommendations as cards
            for idx, (_, movie) in enumerate(recommendations.iterrows(), 1):
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        st.markdown(f"### {idx}. {movie['title']}")
                        st.text(f"Genre: {movie['genre']} | Year: {movie['year']}")

                    with col2:
                        st.markdown(
                            f"<div class='recommendation-score'>⭐ {movie['rating']:.1f}/10</div>",
                            unsafe_allow_html=True,
                        )

                    with col3:
                        if st.button(
                            f"Rate #{idx}",
                            key=f"rate_{movie['movie_id']}",
                        ):
                            st.session_state[
                                f"rating_movie_{movie['movie_id']}"
                            ] = movie

            # Rating section
            st.divider()
            st.subheader("⭐ Rate These Movies")

            for idx, (_, movie) in enumerate(recommendations.iterrows(), 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(movie["title"])
                with col2:
                    rating = st.slider(
                        "Rating",
                        min_value=1.0,
                        max_value=10.0,
                        step=0.5,
                        key=f"slider_{movie['movie_id']}",
                    )
                    if st.button("Save", key=f"save_{movie['movie_id']}"):
                        st.session_state.recommender.rate_movie(
                            person, movie["movie_id"], rating
                        )
                        st.success(f"Rated {rating}/10")


def show_rate_movies():
    st.markdown("## ⭐ Rate Movies")

    known_faces = st.session_state.face_model.get_known_faces()

    if not known_faces:
        st.error("❌ No known faces in database. Register faces first!")
        return

    person = st.selectbox("Select person:", known_faces, key="rate_person")

    st.subheader(f"Rate movies for {person}")

    # Get a sample of movies
    movies = st.session_state.recommender.movies_df.sample(
        min(10, len(st.session_state.recommender.movies_df))
    )

    ratings_data = []

    for _, movie in movies.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(f"{movie['title']} ({movie['year']})")
        with col2:
            rating = st.slider(
                "Rate",
                min_value=0.0,
                max_value=10.0,
                step=0.5,
                key=f"rate_slider_{movie['movie_id']}",
            )
            if rating > 0:
                ratings_data.append(
                    {"movie_id": movie["movie_id"], "rating": rating}
                )

    if st.button("💾 Save Ratings"):
        for item in ratings_data:
            st.session_state.recommender.rate_movie(
                person, item["movie_id"], item["rating"]
            )
        st.success(f"Saved {len(ratings_data)} ratings!")


def show_known_faces():
    st.markdown("## 👥 Known Faces")

    known_faces = st.session_state.face_model.get_known_faces()

    if not known_faces:
        st.info("⚠️ No known faces in database yet.")
        return

    st.subheader(f"Total Known Faces: {len(known_faces)}")

    cols = st.columns(2)

    for i, face in enumerate(known_faces):
        with cols[i % 2]:
            count = st.session_state.face_model.known_face_names.count(face)
            with st.container(border=True):
                st.markdown(f"### 👤 {face}")
                st.text(f"Samples: {count}")

                if st.button(f"Delete {face}", key=f"delete_{face}"):
                    # Note: Delete functionality would require backend changes
                    st.warning(f"Delete {face}? (Not implemented in Streamlit UI)")


def show_browse_movies():
    st.markdown("## 🎬 Browse Movies")

    # Get unique genres
    genres = sorted(st.session_state.recommender.movies_df["genre"].unique())

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_genre = st.selectbox("Select Genre:", genres)

    with col2:
        sort_by = st.selectbox("Sort By:", ["Rating (High to Low)", "Year (Newest)"])

    if selected_genre:
        movies = st.session_state.recommender.get_movies_by_genre(selected_genre)

        if sort_by == "Year (Newest)":
            movies = movies.sort_values("year", ascending=False)

        st.subheader(f"🎬 {selected_genre} Movies ({len(movies)})")

        for _, movie in movies.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**{movie['title']}**")
                    st.caption(f"Year: {movie['year']}")

                with col2:
                    st.metric("Rating", f"{movie['rating']:.1f}/10")

                with col3:
                    if st.button(f"Select", key=f"select_{movie['movie_id']}"):
                        st.session_state[f"selected_movie_{movie['movie_id']}"] = (
                            movie
                        )


if __name__ == "__main__":
    main()
