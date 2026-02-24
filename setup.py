"""
Setup script for Face Recognition Movie Recommender System
Initializes the project and creates necessary directories
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    directories = [
        "data/faces",
        "data",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version OK: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ("cv2", "opencv-python"),
        ("face_recognition", "face_recognition"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("sklearn", "scikit-learn"),
    ]
    
    missing = []
    
    for package, pip_name in required_packages:
        try:
            __import__(package)
            print(f"✓ {pip_name} installed")
        except ImportError:
            print(f"❌ {pip_name} NOT installed")
            missing.append(pip_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n📦 Install with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def initialize_data():
    """Initialize data files"""
    from recommender import MovieRecommender
    
    print("\n📊 Initializing movie database...")
    recommender = MovieRecommender()
    print("✓ Movie database ready")


def main():
    """Main setup function"""
    print("\n" + "=" * 70)
    print("  🎬 Face Recognition Movie Recommender - Setup")
    print("=" * 70 + "\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    print()
    
    # Create directories
    create_directories()
    
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and run setup again")
        return False
    
    print()
    
    # Initialize data
    try:
        initialize_data()
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ Setup complete! Ready to use the application")
    print("=" * 70)
    print("\n🚀 Next steps:")
    print("   1. Run the CLI application:")
    print("      python app.py")
    print("\n   2. Or run the Streamlit UI:")
    print("      streamlit run streamlit_app.py")
    print("\n   3. Or run the complete flow:")
    print("      python app.py --flow")
    print("\n📖 For more information, see README.md\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
