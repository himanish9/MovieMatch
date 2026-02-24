"""
Face Recognition Model
Handles face capture, storage, and recognition
"""

import face_recognition
import cv2
import numpy as np
import os
import pickle
from pathlib import Path
from typing import Optional, Tuple, List


class FaceRecognitionModel:
    def __init__(self, data_dir: str = "data/faces"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.encoding_file = self.data_dir / "face_encodings.pkl"
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_encodings()

    def load_encodings(self):
        """Load existing face encodings from file"""
        if self.encoding_file.exists():
            with open(self.encoding_file, "rb") as f:
                data = pickle.load(f)
                self.known_face_encodings = data["encodings"]
                self.known_face_names = data["names"]
            print(f"✓ Loaded {len(self.known_face_encodings)} face encodings")
        else:
            print("ℹ No existing face encodings found. New dataset will be created.")

    def save_encodings(self):
        """Save face encodings to file"""
        data = {
            "encodings": self.known_face_encodings,
            "names": self.known_face_names,
        }
        with open(self.encoding_file, "wb") as f:
            pickle.dump(data, f)
        print(f"✓ Saved {len(self.known_face_encodings)} face encodings")

    def capture_face_dataset(self, name: str, num_samples: int = 20) -> bool:
        """
        Capture multiple face samples from webcam for a new person
        
        Args:
            name: Person's name
            num_samples: Number of samples to capture
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n📷 Starting face capture for: {name}")
        print(f"   Capturing {num_samples} samples. Look at the camera from different angles.")
        print("   Press 'q' to quit, 's' to capture sample\n")

        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("❌ Error: Could not open webcam")
            return False

        face_encodings_list = []
        sample_count = 0

        while sample_count < num_samples:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            # Draw rectangles and display count
            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"Samples: {sample_count}/{num_samples}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Face Capture - Press 's' to capture, 'q' to quit", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("❌ Capture cancelled")
                video_capture.release()
                cv2.destroyAllWindows()
                return False
            elif key == ord("s"):
                if face_encodings:
                    face_encodings_list.extend(face_encodings)
                    sample_count += 1
                    print(f"   ✓ Sample {sample_count} captured")
                else:
                    print("   ⚠ No face detected. Try again.")

        video_capture.release()
        cv2.destroyAllWindows()

        if face_encodings_list:
            # Add all face encodings to the known faces
            self.known_face_encodings.extend(face_encodings_list)
            self.known_face_names.extend([name] * len(face_encodings_list))
            self.save_encodings()
            print(f"✅ Successfully added {len(face_encodings_list)} samples for {name}")
            return True
        else:
            print("❌ No faces captured")
            return False

    def recognize_faces_from_webcam(
        self, duration: int = 10
    ) -> Optional[str]:
        """
        Recognize faces from webcam for specified duration
        
        Args:
            duration: How long to look for faces (in seconds)
            
        Returns:
            Name of recognized person or None
        """
        if not self.known_face_encodings:
            print("❌ No known faces in database. Please add faces first.")
            return None

        print(f"\n👁️ Starting face recognition for {duration} seconds...")
        print("   Looking for known faces...\n")

        video_capture = cv2.VideoCapture(0)
        process_this_frame = True
        recognized_name = None
        detection_count = {}

        import time
        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = video_capture.read()
            if not ret:
                break

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings,
                        face_encoding,
                        tolerance=0.6,
                    )
                    name = "Unknown"
                    confidence = 0

                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            confidence = 1 - face_distances[best_match_index]

                            # Track detections
                            if name not in detection_count:
                                detection_count[name] = 0
                            detection_count[name] += 1

                    face_names.append((name, confidence))

                process_this_frame = not process_this_frame

            # Display frame with results
            for (top, right, bottom, left), (
                name,
                confidence,
            ) in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                label = (
                    f"{name} ({confidence:.2f})"
                    if name != "Unknown"
                    else "Unknown"
                )
                cv2.putText(
                    frame,
                    label,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2,
                )

            cv2.imshow("Face Recognition - Press 'q' to quit", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Return most detected person
        if detection_count:
            recognized_name = max(detection_count, key=detection_count.get)
            print(f"\n✅ Recognized: {recognized_name}")
            return recognized_name
        else:
            print("\n❌ No known face recognized")
            return None

    def get_known_faces(self) -> List[str]:
        """Get list of unique known faces"""
        return list(set(self.known_face_names))

    def detect_emotion(self, frame) -> str:
        """
        Person-specific emotion detection using simple, direct rules:
        1. Visible teeth → Happy
        2. Strongly raised eyebrows with tension → Angry
        3. No teeth + relaxed face → Neutral
        
        Args:
            frame: Input video frame
            
        Returns:
            Detected emotion: 'happy', 'angry', or 'neutral'
        """
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            
            # Detect face locations
            face_locations = face_recognition.face_locations(gray_frame)
            
            if not face_locations:
                return 'neutral'
            
            top, right, bottom, left = face_locations[0]
            face_height = bottom - top
            face_width = right - left
            face_region = gray_frame[top:bottom, left:right]
            
            # RULE 1: Check for visible teeth (Happy indicator)
            mouth_top = int(face_height * 0.62)
            mouth_bottom = int(face_height * 0.92)
            mouth_left = int(face_width * 0.2)
            mouth_right = int(face_width * 0.8)
            
            if mouth_bottom > face_height:
                mouth_bottom = face_height
            
            mouth_region = face_region[mouth_top:mouth_bottom, mouth_left:mouth_right]
            
            # Detect bright pixels (white teeth) in mouth region
            bright_teeth_pixels = np.sum(mouth_region > 200)
            total_mouth_pixels = mouth_region.shape[0] * mouth_region.shape[1]
            teeth_visibility_ratio = bright_teeth_pixels / total_mouth_pixels if total_mouth_pixels > 0 else 0
            
            # HIGH PRIORITY: If teeth are clearly visible → Happy
            if teeth_visibility_ratio > 0.15:
                return 'happy'
            
            # RULE 2: Check for raised eyebrows with tension (Angry indicator)
            eyebrow_top = int(face_height * 0.05)
            eyebrow_bottom = int(face_height * 0.2)
            eyebrow_left = int(face_width * 0.1)
            eyebrow_right = int(face_width * 0.9)
            
            eyebrow_region = face_region[eyebrow_top:eyebrow_bottom, eyebrow_left:eyebrow_right]
            eyebrow_variance = np.var(eyebrow_region) if eyebrow_region.size > 0 else 0
            
            # Detect edges/tension lines in eyebrow region (furrowed = high density)
            eyebrow_edges = cv2.Canny(eyebrow_region, 30, 100)
            eyebrow_edge_density = np.count_nonzero(eyebrow_edges) / (eyebrow_region.shape[0] * eyebrow_region.shape[1]) if eyebrow_region.size > 0 else 0
            
            # Strong eyebrow tension (furrowed) + high edge density → Angry
            if eyebrow_variance > 550 and eyebrow_edge_density > 0.09:
                return 'angry'
            
            # RULE 3: No teeth visible + relaxed face → Neutral
            # This is the default when neither happy nor angry rules apply
            return 'neutral'
            
        except Exception as e:
            print(f"[v0] Emotion detection error: {str(e)}")
            return 'neutral'

    def recognize_with_emotion(self, duration: int = 10) -> Tuple[Optional[str], str]:
        """
        Recognize faces and detect emotion simultaneously
        
        Args:
            duration: How long to look for faces (in seconds)
            
        Returns:
            Tuple of (recognized_name, detected_emotion)
        """
        if not self.known_face_encodings:
            print("❌ No known faces in database. Please add faces first.")
            return None, 'neutral'

        print(f"\n👁️ Starting face recognition & emotion detection for {duration} seconds...")
        print("   Looking for known faces...\n")

        video_capture = cv2.VideoCapture(0)
        process_this_frame = True
        recognized_name = None
        detected_emotion = 'neutral'
        detection_count = {}
        emotion_count = {'happy': 0, 'angry': 0, 'neutral': 0}

        import time
        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Detect emotion from current frame
            emotion = self.detect_emotion(frame)
            emotion_count[emotion] += 1

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings,
                        face_encoding,
                        tolerance=0.6,
                    )
                    name = "Unknown"
                    confidence = 0

                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            confidence = 1 - face_distances[best_match_index]

                            if name not in detection_count:
                                detection_count[name] = 0
                            detection_count[name] += 1

                    face_names.append((name, confidence))

                process_this_frame = not process_this_frame

            # Display frame with results
            for (top, right, bottom, left), (name, confidence) in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                label = f"{name} ({confidence:.2f})" if name != "Unknown" else "Unknown"
                cv2.putText(
                    frame,
                    label,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2,
                )
                
                # Display detected emotion
                emotion_label = f"Emotion: {emotion}"
                cv2.putText(
                    frame,
                    emotion_label,
                    (left, bottom + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2,
                )

            cv2.imshow("Face Recognition & Emotion Detection - Press 'q' to quit", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Return most detected person and emotion
        if detection_count:
            recognized_name = max(detection_count, key=detection_count.get)
            detected_emotion = max(emotion_count, key=emotion_count.get)
            print(f"\n✅ Recognized: {recognized_name}")
            print(f"😊 Detected Emotion: {detected_emotion}")
            return recognized_name, detected_emotion
        else:
            detected_emotion = max(emotion_count, key=emotion_count.get)
            print(f"\n❌ No known face recognized")
            print(f"😊 Detected Emotion: {detected_emotion}")
            return None, detected_emotion
