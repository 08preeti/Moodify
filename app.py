import streamlit as st
import os
import tempfile
from emotion_detector import detect_emotion_and_get_song

# Set page config
st.set_page_config(page_title="Moodify 🎵", page_icon="🎧", layout="centered")

# Emoji mapping based on emotion
emoji_map = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😡",
    "surprise": "😲",
    "fear": "😱",
    "disgust": "🤢",
    "neutral": "😐"
}

# Header
st.markdown("<h1 style='text-align: center;'>🎧 Moodify</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Detect your mood from a selfie and get a perfect song! 🎵</h4>", unsafe_allow_html=True)
st.markdown("---")

# Upload section
uploaded_file = st.file_uploader("📤 Upload your selfie (jpg/jpeg/png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.read())
        image_path = tmp_file.name

    st.image(image_path, caption="📷 Your Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing emotion... 😶"):
        emotion, song_path = detect_emotion_and_get_song(image_path)

    st.markdown("---")

    if emotion:
        emoji = emoji_map.get(emotion.lower(), "🎭")
        st.markdown(f"<h2 style='text-align: center;'>Detected Emotion: {emoji} <br><span style='color:#4CAF50'>{emotion.upper()}</span></h2>", unsafe_allow_html=True)

        if song_path and os.path.exists(song_path):
            st.markdown(f"<h4 style='text-align: center;'>🎶 Here’s a song for your mood</h4>", unsafe_allow_html=True)
            st.audio(song_path, format="audio/mp3")
        else:
            st.warning("No matching song found for this emotion.")
    else:
        st.error("😕 Could not detect emotion. Try another image.")

    st.markdown("---")
    if st.button("🔁 Try Another Image"):
        st.experimental_rerun()
else:
    st.info("👆 Please upload an image file (preferably a selfie).")

