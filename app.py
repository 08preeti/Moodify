import streamlit as st
import numpy as np
import cv2
from deepface import DeepFace
import tempfile
import os
import random
from emotion_detector import detect_emotion_and_get_song

st.set_page_config(page_title="Moodify - Emotion Based Music Player 🎵", layout="centered")

st.title("🎵 Moodify: Emotion-Based Music Player")
st.markdown("Smile, frown, or just be you. We'll find the right tune for your mood!")

# Capture image from webcam
img_file_buffer = st.camera_input("📸 Capture your mood")

if img_file_buffer is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(img_file_buffer.read())
        temp_image_path = temp_file.name

    # Detect emotion and play song
    with st.spinner("Detecting emotion..."):
        emotion, song_path = detect_emotion_and_get_song(temp_image_path)

    if emotion:
        st.success(f"Detected Emotion: **{emotion.capitalize()}**")
        if song_path:
            st.audio(song_path, format="audio/mp3")
            st.caption(f"Now playing: 🎶 `{os.path.basename(song_path)}`")
        else:
            st.warning("No songs found for this emotion.")
    else:
        st.error("Could not detect emotion. Try again!")






