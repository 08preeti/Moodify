import cv2
from deepface import DeepFace
import pygame
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import os
import random
from PIL import Image, ImageTk

# 🎵 Initialize pygame mixer
pygame.mixer.init()

# 🎤 Initialize voice engine
engine = pyttsx3.init()

# 🎭 Emoji mapping
emotion_emojis = {
    "angry": "😠",
    "disgust": "🤢",
    "fear": "😱",
    "happy": "😄",
    "sad": "😢",
    "surprise": "😮",
    "neutral": "😐"
}

# 🎤 Speak emotion aloud
def speak_emotion(emotion):
    engine.say(f"You look {emotion}")
    engine.runAndWait()

# 📸 Start webcam
cap = cv2.VideoCapture(0)

# 🎨 GUI setup
root = tk.Tk()
root.title("🎵 Moodify - Emotion Music Player")
root.geometry("700x600")
root.configure(bg="#f0f8ff")

# 🖼️ Load background image (optional)
# bg_image = Image.open("your_background.jpg")
# bg_photo = ImageTk.PhotoImage(bg_image)
# bg_label = tk.Label(root, image=bg_photo)
# bg_label.place(relwidth=1, relheight=1)

# 🧠 Main label
title_label = tk.Label(root, text="🎵 Moodify - Emotion Detector", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="purple")
title_label.pack(pady=10)

emotion_label = tk.Label(root, text="🤖 Show your face & click Detect", font=("Arial", 16), bg="#f0f8ff", fg="black")
emotion_label.pack(pady=10)

# 📊 Frame for emotion scores
emotion_frame = tk.Frame(root, bg="#f0f8ff")
emotion_frame.pack(pady=10)

# 🎥 Frame for webcam preview
video_frame = tk.Label(root)
video_frame.pack(pady=10)

# 🔍 Detect Emotion
def detect_emotion():
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Webcam not accessible")
        return

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        if isinstance(result, list) and len(result) > 0 and 'dominant_emotion' in result[0]:
            emotion = result[0]['dominant_emotion']
            emotion_scores = result[0]['emotion']

            # 🧠 Update label
            emotion_label.config(text=f"{emotion_emojis.get(emotion, '')} You look {emotion.upper()}", fg="blue")
            speak_emotion(emotion)

            # 🧽 Clear old values
            for widget in emotion_frame.winfo_children():
                widget.destroy()

            # 📊 Display all emotions
            for emo, val in emotion_scores.items():
                row = tk.Frame(emotion_frame, bg="#f0f8ff")
                row.pack(anchor='w', padx=30)

                emoji = emotion_emojis.get(emo, '')
                label = tk.Label(row, text=f"{emoji} {emo.capitalize()}: {val:.2f}%", font=("Arial", 11), bg="#f0f8ff")
                label.pack(anchor='w')

            # 🎶 Play music
            music_folder = os.path.join("emotion_detector", "music", emotion)
            if os.path.exists(music_folder):
                songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
                if songs:
                    song_path = os.path.join(music_folder, random.choice(songs))
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    print(f"▶️ Playing: {song_path}")
                else:
                    messagebox.showinfo("No Music", f"No .mp3 files in {emotion} folder")
            else:
                messagebox.showinfo("Missing Folder", f"No folder for emotion: {emotion}")
        else:
            messagebox.showerror("Detection Failed", "Could not detect emotion properly")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ⏹️ Stop Music
def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        messagebox.showinfo("Music", "Music stopped")
    else:
        messagebox.showinfo("Music", "No music is playing")

# 📸 Update video feed
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_frame.imgtk = imgtk
        video_frame.configure(image=imgtk)
    video_frame.after(10, update_frame)

update_frame()

# 🎛️ Buttons
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=20)

detect_button = tk.Button(button_frame, text="🔍 Detect Emotion", font=("Arial", 12), command=detect_emotion, bg="lightgreen")
detect_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="⏹️ Stop Music", font=("Arial", 12), command=stop_music, bg="tomato")
stop_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(button_frame, text="❌ Exit", font=("Arial", 12), command=root.destroy, bg="gray")
exit_button.grid(row=0, column=2, padx=10)

# 🚀 Start GUI loop
root.mainloop()
cap.release()
cv2.destroyAllWindows()
