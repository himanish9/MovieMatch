"""
Face Recognition Movie Recommender System
Main application with CLI interface
"""

import sys
from model import FaceRecognitionModel
from recommender import MovieRecommender


def print_banner():
    """Print application banner"""
    print("\n" + "=" * 70)
    print("    🎬 FACE RECOGNITION MOVIE RECOMMENDER SYSTEM 🎬")
    print("=" * 70)
    print()


def print_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU")
    print("-" * 70)
    print("1. Register New Face (Add new person to database)")
    print("2. Recognize Face (Identify person from webcam)")
    print("3. Get Movie Recommendations (For a specific person)")
    print("4. Rate Movie (Record ratings for recommendations)")
    print("5. View All Known Faces")
    print("6. View Movies by Genre")
    print("7. Exit")
    print("-" * 70)


def register_new_face(face_model: FaceRecognitionModel):
    """Register a new person's face"""
    print("\n" + "=" * 70)
    print("📝 REGISTER NEW FACE")
    print("=" * 70)

    name = input("\nEnter person's name: ").strip()

    if not name:
        print("❌ Name cannot be empty")
        return

    # Check if person already exists
    if name in face_model.get_known_faces():
        response = (
            input(
                f"⚠️  {name} already exists. Add more samples? (y/n): "
            )
            .strip()
            .lower()
        )
        if response != "y":
            return

    num_samples = input("Number of samples to capture (default 20): ").strip()
    try:
        num_samples = int(num_samples) if num_samples else 20
    except ValueError:
        num_samples = 20

    if face_model.capture_face_dataset(name, num_samples):
        print(f"\n✅ Successfully registered {name}")
    else:
        print(f"\n❌ Failed to register {name}")


def recognize_face(face_model: FaceRecognitionModel) -> str:
    """Recognize a person from webcam"""
    print("\n" + "=" * 70)
    print("👁️ FACE RECOGNITION")
    print("=" * 70)

    known_faces = face_model.get_known_faces()
    if not known_faces:
        print("\n❌ No known faces in database. Please register faces first.")
        return None

    duration = input("Duration to capture (seconds, default 10): ").strip()
    try:
        duration = int(duration) if duration else 10
    except ValueError:
        duration = 10

    recognized_name = face_model.recognize_faces_from_webcam(duration)
    return recognized_name


def get_recommendations(
    face_model: FaceRecognitionModel, recommender: MovieRecommender
):
    """Get movie recommendations for a person"""
    print("\n" + "=" * 70)
    print("🍿 GET RECOMMENDATIONS")
    print("=" * 70)

    known_faces = face_model.get_known_faces()

    if not known_faces:
        print("\n❌ No known faces in database.")
        return

    print("\nKnown faces:")
    for i, face in enumerate(known_faces, 1):
        print(f"  {i}. {face}")

    choice = input("\nSelect person (number or name): ").strip()

    person = None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(known_faces):
            person = known_faces[idx]
    except ValueError:
        if choice in known_faces:
            person = choice

    if not person:
        print("❌ Invalid selection")
        return

    # Option to use real-time recognition
    use_recognition = (
        input(f"Use face recognition to confirm? (y/n): ").strip().lower()
    )
    if use_recognition == "y":
        recognized = recognize_face(face_model)
        if recognized and recognized != person:
            print(f"\n⚠️  Recognized {recognized}, but using {person}")

    # Get recommendations
    recommendations = recommender.get_recommendations(person, top_n=4)
    recommender.display_recommendations(person, recommendations)

    # Option to rate movies
    rate = input("\nWould you like to rate any of these movies? (y/n): ").strip().lower()
    if rate == "y":
        rate_movies(person, recommendations, recommender)


def rate_movies(user: str, movies_df, recommender: MovieRecommender):
    """Rate movies for improved recommendations"""
    print("\n" + "-" * 70)
    print("⭐ RATE MOVIES")
    print("-" * 70)

    while True:
        movie_num = input(
            "Enter movie number to rate (1-4) or '0' to skip: "
        ).strip()
        try:
            movie_num = int(movie_num)
            if movie_num == 0:
                break
            if 1 <= movie_num <= len(movies_df):
                movie = movies_df.iloc[movie_num - 1]
                rating = input(
                    f"Rate '{movie['title']}' (1-10): "
                ).strip()
                try:
                    rating = float(rating)
                    if 1 <= rating <= 10:
                        recommender.rate_movie(user, movie["movie_id"], rating)
                        print(f"✓ Rated '{movie['title']}': {rating}/10")
                    else:
                        print("❌ Rating must be between 1-10")
                except ValueError:
                    print("❌ Invalid rating")
            else:
                print("❌ Invalid movie number")
        except ValueError:
            print("❌ Invalid input")


def view_known_faces(face_model: FaceRecognitionModel):
    """Display all known faces"""
    print("\n" + "=" * 70)
    print("👥 KNOWN FACES IN DATABASE")
    print("=" * 70)

    known_faces = face_model.get_known_faces()

    if not known_faces:
        print("\n⚠️  No known faces in database yet.")
        return

    print(f"\nTotal known faces: {len(known_faces)}\n")
    for i, face in enumerate(known_faces, 1):
        count = face_model.known_face_names.count(face)
        print(f"  {i}. {face} ({count} samples)")

    print("\n" + "=" * 70)


def view_movies_by_genre(recommender: MovieRecommender):
    """View movies by genre"""
    print("\n" + "=" * 70)
    print("🎬 BROWSE MOVIES BY GENRE")
    print("=" * 70)

    # Get unique genres
    genres = recommender.movies_df["genre"].unique()
    genres = sorted(genres)

    print("\nAvailable genres:")
    for i, genre in enumerate(genres, 1):
        count = len(recommender.movies_df[recommender.movies_df["genre"] == genre])
        print(f"  {i}. {genre} ({count} movies)")

    choice = input("\nSelect genre (number): ").strip()

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(genres):
            genre = genres[idx]
            movies = recommender.get_movies_by_genre(genre)

            print(f"\n🎬 TOP MOVIES IN {genre.upper()}")
            print("-" * 70)
            for i, (_, movie) in enumerate(movies.head(10).iterrows(), 1):
                print(
                    f"{i}. {movie['title']} ({movie['year']}) - {movie['rating']}/10"
                )
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")


def run_full_flow():
    """Run the complete flow: capture -> recognize -> recommend"""
    print("\n" + "=" * 70)
    print("🚀 FULL FLOW: Capture → Recognize → Recommend")
    print("=" * 70)

    face_model = FaceRecognitionModel()
    recommender = MovieRecommender()

    # Step 1: Capture or select face
    action = (
        input(
            "\nCapture new face (c) or recognize existing (r)? (c/r): "
        )
        .strip()
        .lower()
    )

    if action == "c":
        register_new_face(face_model)
        person = input("Enter the name you just registered: ").strip()
    elif action == "r":
        person = recognize_face(face_model)
    else:
        print("❌ Invalid action")
        return

    if not person:
        print("❌ Could not identify person")
        return

    print(f"\n✅ Working with: {person}")

    # Step 2: Get recommendations
    print("\n🎬 Generating personalized recommendations...")
    recommendations = recommender.get_recommendations(person, top_n=4)
    recommender.display_recommendations(person, recommendations)

    # Step 3: Option to rate
    rate = input(
        "\nWould you like to rate these movies to improve recommendations? (y/n): "
    ).strip().lower()
    if rate == "y":
        rate_movies(person, recommendations, recommender)


def main():
    """Main application loop"""
    print_banner()

    face_model = FaceRecognitionModel()
    recommender = MovieRecommender()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            register_new_face(face_model)
        elif choice == "2":
            recognized = recognize_face(face_model)
            if recognized:
                # Auto-recommend if recognized
                auto_rec = (
                    input(
                        f"\nGet recommendations for {recognized}? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if auto_rec == "y":
                    recommendations = recommender.get_recommendations(
                        recognized, top_n=4
                    )
                    recommender.display_recommendations(recognized, recommendations)
        elif choice == "3":
            get_recommendations(face_model, recommender)
        elif choice == "4":
            print("\n" + "=" * 70)
            print("⭐ RATE MOVIES")
            print("=" * 70)
            user = input("Enter person's name: ").strip()
            if user:
                # Show some movies to rate
                movies = recommender.movies_df.sample(
                    min(5, len(recommender.movies_df))
                )
                rate_movies(user, movies, recommender)
        elif choice == "5":
            view_known_faces(face_model)
        elif choice == "6":
            view_movies_by_genre(recommender)
        elif choice == "7":
            print("\n👋 Thank you for using the Face Recognition Movie Recommender!")
            print("=" * 70 + "\n")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Face Recognition Movie Recommender System"
    )
    parser.add_argument(
        "--flow",
        action="store_true",
        help="Run the complete capture→recognize→recommend flow",
    )

    args = parser.parse_args()

    if args.flow:
        run_full_flow()
    else:
        main()
