import streamlit as st
import os
import tempfile
from emotion_detector import detect_emotion_and_get_song

# Set page config
st.set_page_config(page_title="Moodify 🎵", page_icon="🎧", layout="centered")

# Emoji mapping based on emotion
emoji_map = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "surprise": "😲",
    "fear": "😱",
    "disgust": "🤢",
    "neutral": "😐"
}

# Title
st.title("🎶 Moodify - Detect Your Mood & Play Music")

# Instructions
st.markdown("Upload a selfie or photo of a face and let Moodify play a song that matches your emotion! 📸🎵")

# Upload file
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.read())
        image_path = tmp_file.name

    # Show image preview
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Detect emotion and get song
    emotion, song_path = detect_emotion_and_get_song(image_path)

    if emotion:
        emoji = emoji_map.get(emotion.lower(), "")
        st.success(f"**Detected Emotion:** `{emotion.upper()}` {emoji}")

        if song_path and os.path.exists(song_path):
            st.audio(song_path, format="audio/mp3")
        else:
            st.warning("No song available for this emotion 😔")

    else:
        st.error("Emotion detection failed. Try another image.")

    # Retry button
    if st.button("🔁 Try Another Image"):
        st.experimental_rerun()
