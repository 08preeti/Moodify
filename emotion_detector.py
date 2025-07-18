from deepface import DeepFace
import os
import random

def detect_emotion_and_get_song(image_path):
    try:
        result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)

        # Make sure result is a list and has at least one entry
        if isinstance(result, list) and len(result) > 0:
            emotion = result[0]['dominant_emotion']
        elif isinstance(result, dict) and 'dominant_emotion' in result:
            emotion = result['dominant_emotion']
        else:
            print("[ERROR] Unexpected result from DeepFace:", result)
            return None, None

        print(f"[LOG] Detected Emotion: {emotion}")

        # Locate folder with songs for this emotion
        music_folder = os.path.join("emotion_detector", "music", emotion)

        if os.path.exists(music_folder):
            songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
            if songs:
                selected_song = random.choice(songs)
                song_path = os.path.join(music_folder, selected_song)
                return emotion, song_path
            else:
                print(f"[LOG] No songs in folder for {emotion}")
                return emotion, None
        else:
            print(f"[LOG] Folder not found for emotion: {emotion}")
            return emotion, None

    except Exception as e:
        print(f"[ERROR] Emotion detection failed: {e}")
        return None, None



