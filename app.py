import streamlit as st
import numpy as np
from deepface import DeepFace
import tempfile
import os
import random

# Set page config
st.set_page_config(page_title="🎭 Moodify - Emotion Based Music Player", page_icon="🎵", layout="centered")

# Title and instructions
st.title("🎭 Moodify")
st.markdown("#### Detect your emotion via webcam and let Moodify play a song to match your mood 🎶")

# Background style
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right, #f9f7f7, #e4f0f5);
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# Camera input (built-in in Streamlit)
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

        # Music path setup
        base_music_dir = os.path.join(os.getcwd(), "emotion_detector", "music")
        music_folder = os.path.join(base_music_dir, emotion.lower())

        if os.path.exists(music_folder):
            songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
            if songs:
                song_file = random.choice(songs)
                song_path = os.path.join(music_folder, song_file)

                # Streamlit audio playback
                audio_file = open(song_path, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("⚠️ No songs found in this emotion folder.")
        else:
            st.warning(f"⚠️ Folder not found for emotion: `{emotion}`")
    except Exception as e:
        st.error(f"❌ Error detecting emotion: {e}")







