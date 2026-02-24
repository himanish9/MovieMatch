"""
Configuration file for Face Recognition Movie Recommender System
Customize settings here without modifying the core code
"""

# ============================================================================
# FACE RECOGNITION SETTINGS
# ============================================================================

# Face recognition tolerance (0.0-1.0)
# Lower = stricter matching (fewer false positives)
# Higher = lenient matching (more false negatives)
# Recommended range: 0.5-0.7
FACE_RECOGNITION_TOLERANCE = 0.6

# Default number of samples to capture during registration
DEFAULT_FACE_SAMPLES = 20

# Video frame resize factor for faster processing
# 0.25 = 25% of original size (faster, lower accuracy)
# 1.0 = Full size (slower, higher accuracy)
VIDEO_FRAME_SCALE = 0.25

# Process every Nth frame for faster recognition
# 1 = Process every frame (slower but accurate)
# 2 = Process every 2nd frame (faster)
FRAME_SKIP = 1

# Default camera index (0 = default webcam)
CAMERA_INDEX = 0


# ============================================================================
# RECOMMENDATION SETTINGS
# ============================================================================

# Default number of recommendations to show
DEFAULT_RECOMMENDATIONS = 4

# Maximum number of recommendations to show
MAX_RECOMMENDATIONS = 10

# Recommendation algorithm weights
# These must sum to 1.0
RECOMMENDATION_WEIGHTS = {
    "genre_preference": 0.5,      # User's preferred genres
    "movie_rating": 0.35,         # Base movie quality
    "recency": 0.15,              # Recent movies boost
}

# Minimum rating to consider a movie "highly rated"
MIN_HIGH_RATING = 7.0

# Number of top genres to consider for recommendations
TOP_GENRES_COUNT = 3


# ============================================================================
# STORAGE SETTINGS
# ============================================================================

# Directory to store face encodings
FACES_DATA_DIR = "data/faces"

# Face encodings pickle file name
FACE_ENCODINGS_FILE = "face_encodings.pkl"

# Movie database CSV file
MOVIES_CSV_FILE = "data/movies.csv"

# User ratings JSON file
USER_RATINGS_FILE = "data/user_ratings.json"

# Create directories if they don't exist
CREATE_MISSING_DIRS = True


# ============================================================================
# UI SETTINGS
# ============================================================================

# Terminal display settings
TERMINAL_WIDTH = 70

# Show debug information
DEBUG_MODE = False

# Colors for terminal output (ANSI codes)
COLORS = {
    "success": "\033[92m",      # Green
    "error": "\033[91m",        # Red
    "warning": "\033[93m",      # Yellow
    "info": "\033[94m",         # Blue
    "reset": "\033[0m",         # Reset
}

# Emojis for terminal
EMOJIS = {
    "face": "👤",
    "camera": "📷",
    "recognition": "👁️",
    "movie": "🎬",
    "popcorn": "🍿",
    "star": "⭐",
    "check": "✓",
    "cross": "❌",
    "warning": "⚠️",
    "info": "ℹ",
    "rating": "⭐",
    "genre": "🎯",
    "database": "💾",
}


# ============================================================================
# WEBCAM SETTINGS
# ============================================================================

# Display webcam feed window
SHOW_WEBCAM_WINDOW = True

# Window title for face capture
CAPTURE_WINDOW_TITLE = "Face Capture - Press 's' to capture, 'q' to quit"

# Window title for face recognition
RECOGNITION_WINDOW_TITLE = "Face Recognition - Press 'q' to quit"

# Face rectangle color (BGR format)
FACE_RECT_COLOR = (0, 255, 0)  # Green
FACE_UNKNOWN_COLOR = (0, 0, 255)  # Red

# Face rectangle thickness
FACE_RECT_THICKNESS = 2

# Default recognition duration (seconds)
DEFAULT_RECOGNITION_DURATION = 10


# ============================================================================
# MOVIE DATASET SETTINGS
# ============================================================================

# Sample movie data will be created if no CSV exists
CREATE_SAMPLE_MOVIES = True

# Genres for the movie database
AVAILABLE_GENRES = [
    "Drama",
    "Action",
    "Sci-Fi",
    "Comedy",
    "Thriller",
    "Romance",
    "Adventure",
    "Animation",
    "Crime",
    "War",
    "Biography",
]

# Movie rating range
MIN_MOVIE_RATING = 1.0
MAX_MOVIE_RATING = 10.0


# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Enable GPU acceleration if available (CUDA)
USE_GPU = False

# Number of CPU threads to use
NUM_THREADS = -1  # -1 = Auto detect

# Batch size for face processing
BATCH_SIZE = 32


# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Enable detailed logging
ENABLE_LOGGING = True

# Log file location
LOG_FILE = "face_recommender.log"

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_weights():
    """Validate that recommendation weights sum to 1.0"""
    total = sum(RECOMMENDATION_WEIGHTS.values())
    if abs(total - 1.0) > 0.001:
        raise ValueError(
            f"Recommendation weights must sum to 1.0, got {total}"
        )


def get_config_summary():
    """Get a summary of current configuration"""
    return {
        "Face Recognition": {
            "Tolerance": FACE_RECOGNITION_TOLERANCE,
            "Default Samples": DEFAULT_FACE_SAMPLES,
            "Frame Scale": VIDEO_FRAME_SCALE,
        },
        "Recommendations": {
            "Default Count": DEFAULT_RECOMMENDATIONS,
            "Weights": RECOMMENDATION_WEIGHTS,
        },
        "Storage": {
            "Faces Dir": FACES_DATA_DIR,
            "Movies CSV": MOVIES_CSV_FILE,
            "Ratings JSON": USER_RATINGS_FILE,
        },
        "UI": {
            "Debug Mode": DEBUG_MODE,
            "Show Webcam": SHOW_WEBCAM_WINDOW,
        },
    }


# Validate configuration on import
validate_weights()


if __name__ == "__main__":
    # Print current configuration
    import json
    summary = get_config_summary()
    print("=" * 70)
    print("CURRENT CONFIGURATION")
    print("=" * 70)
    print(json.dumps(summary, indent=2))
