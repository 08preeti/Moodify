import streamlit as st
import numpy as np
from deepface import DeepFace
import tempfile
import os
import random

st.set_page_config(page_title="🎭 Moodify", page_icon="🎵")

st.title("🎭 Moodify - Emotion Based Music Player")
st.markdown("#### Detect your emotion via webcam and let Moodify play a song to match your mood 🎶")

# Background styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

img_data = st.camera_input("📸 Capture your image")

if img_data is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(img_data.getvalue())
        img_path = tmp_file.name

    st.success("Image captured! Detecting emotion...")

    try:
        result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        st.subheader(f"😃 Detected Emotion: **{emotion.capitalize()}**")
        st.write("📊 Emotion Scores:", result[0]['emotion'])

        # Play song
        music_folder = os.path.join("emotion_detector", "music", emotion.lower())
        if os.path.exists(music_folder):
            songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
            if songs:
                song_file = random.choice(songs)
                song_path = os.path.join(music_folder, song_file)
                st.audio(song_path, format='audio/mp3', start_time=0)
            else:
                st.warning("⚠️ No .mp3 files found for this emotion.")
        else:
            st.warning(f"⚠️ No folder found for emotion: `{emotion}`")
    except Exception as e:
        st.error(f"❌ Error detecting emotion: {e}")








