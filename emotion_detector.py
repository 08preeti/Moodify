import cv2
from deepface import DeepFace
import pygame
import os
import random

# Initialize pygame mixer
pygame.mixer.init()

# Start webcam
cap = cv2.VideoCapture(0)
print("🎥 Webcam is starting...")
print("😊 Show emotion and press 'q' to detect OR press 's' to stop the music")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Webcam not working")
        break

    cv2.putText(frame, "Press 'q' to detect / 's' to stop music", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Moodify", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("🔍 Detecting emotion...")
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if result and isinstance(result, list):
                emotion = result[0]['dominant_emotion']
                print(f"✅ Detected Emotion: {emotion}")
                print(f"📊 All emotions: {result[0]['emotion']}")

                music_folder = os.path.join("emotion_detector", "music", emotion.lower())

                if os.path.exists(music_folder):
                    songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
                    if songs:
                        song_file = random.choice(songs)
                        song_path = os.path.join(music_folder, song_file)
                        print(f"🎵 Playing: {song_file}")

                        pygame.mixer.music.load(song_path)
                        pygame.mixer.music.play()
                    else:
                        print(f"🚫 No .mp3 files in: {music_folder}")
                else:
                    print(f"🚫 No folder found for emotion: {emotion}")
            else:
                print("❌ Could not detect a face or emotion.")

        except Exception as e:
            print(f"❌ Error: {e}")

    elif key == ord('s'):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("⏹️ Music stopped manually")
        else:
            print("⏹️ No music is playing")

    elif key == 27:  # ESC key
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()



