import tkinter as tk
from tkinter import messagebox
import threading
import sounddevice as sd
import numpy as np
import vosk
import queue
import json
import cv2
from deepface import DeepFace
import pyttsx3
import time
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
from fpdf import FPDF
matplotlib.use('Agg')  

MODEL_PATH = "vosk-model-small-en-us-0.15"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Vosk model not found.")

q = queue.Queue()
engine = pyttsx3.init()

questions = [
    "Over the last two weeks, how often have you had little interest or pleasure in doing things?",
    "How often have you felt down, depressed, or hopeless?",
    "Do you have trouble falling or staying asleep, or sleeping too much?",
    "Have you felt tired or had little energy?",
    "How often have you had poor appetite or overeating?",
    "Do you feel bad about yourself or that you are a failure?",
    "Do you have trouble concentrating on things?",
    "Have you been moving or speaking slowly or being fidgety?",
    "Have you had thoughts that you'd be better off dead, or of hurting yourself?"
]

answers = []
current_question = 0
cap = cv2.VideoCapture(0)


def record_audio(duration=5, samplerate=16000):
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return audio

def recognize_speech(audio, samplerate=16000):
    model = vosk.Model(MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, samplerate)
    rec.AcceptWaveform(audio.tobytes())
    result = json.loads(rec.Result())
    return result.get("text", "")

def analyze_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No Face"


def update_video():
    ret, frame = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.image = imgtk
        video_label.configure(image=imgtk)
    video_label.after(30, update_video)

def ask_question():
    global current_question

    if current_question >= len(questions):
        show_results()
        return

    question = questions[current_question]
    question_label.config(text=f"Q{current_question+1}: {question}")
    engine.say(question)
    engine.runAndWait()

    threading.Thread(target=process_answer).start()

def process_answer():
    global current_question
    status_label.config(text="Recording your response...")
    audio = record_audio()
    text = recognize_speech(audio)

    status_label.config(text="Analyzing facial emotion...")
    ret, frame = cap.read()
    emotion = analyze_emotion(frame)

    answers.append({
        "question": questions[current_question],
        "answer_text": text,
        "emotion": emotion
    })

    response_label.config(text=f"You said: {text}\nDetected Emotion: {emotion}")
    status_label.config(text="Done. Say 'next' to continue or press Start.")
    current_question += 1


def show_results():
    cap.release()
    summary = "Results:\n\n"
    score = 0
    emotion_count = {}
    for idx, ans in enumerate(answers):
        summary += f"Q{idx+1}: {ans['question']}\n"
        summary += f"You said: {ans['answer_text']}\nEmotion: {ans['emotion']}\n\n"
        if ans['emotion'] in ['sad', 'angry', 'fear']:
            score += 1
        emotion_count[ans['emotion']] = emotion_count.get(ans['emotion'], 0) + 1

    summary += f"Estimated Depression Risk Score: {score}/9\n"
    if score >= 5:
        recommendation = "⚠️ Moderate to high risk of depression. Please consider seeking professional help."
    else:
        recommendation = "✅ Low risk of depression."

    summary += f"\n{recommendation}"

  
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write(summary)


    emotions = list(emotion_count.keys())
    counts = list(emotion_count.values())
    plt.figure(figsize=(6, 4))
    plt.bar(emotions, counts, color='orange')
    plt.title("Detected Emotions During Interview")
    plt.xlabel("Emotion")
    plt.ylabel("Frequency")
    plt.tight_layout()
    chart_path = "emotion_chart.png"
    plt.savefig(chart_path)

  
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)

    if os.path.exists(chart_path):
        pdf.image(chart_path, x=10, w=pdf.w - 20)

    pdf.output("report.pdf")

    messagebox.showinfo("Assessment Complete", summary)
    root.destroy()



root = tk.Tk()
root.title("🧠 Depression Screener - Voice + Emotion")
root.geometry("720x640")
root.configure(bg="#1e1e1e")

style = {"bg": "#1e1e1e", "fg": "white", "font": ("Arial", 13)}

question_label = tk.Label(root, text="Press Start to begin the assessment.", wraplength=650, **style)
question_label.pack(pady=10)

video_label = tk.Label(root)
video_label.pack()

response_label = tk.Label(root, text="", wraplength=650, fg="#7dd3fc", bg="#1e1e1e")
response_label.pack(pady=10)

status_label = tk.Label(root, text="", fg="#a3e635", bg="#1e1e1e")
status_label.pack(pady=5)

start_button = tk.Button(root, text="🎙️ Start Assessment", font=("Arial", 12), bg="#10b981", fg="white", command=ask_question)
start_button.pack(pady=10)

update_video()
root.mainloop()
