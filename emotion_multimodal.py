import cv2
from deepface import DeepFace
import threading
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from textblob import TextBlob
import pyttsx3
from collections import Counter
import time


speech_result = ""
speech_emotion = "Neutral"
face_emotion = "Neutral"
face_confidence = 0
face_emotions_counter = Counter()
emoji_map = {
    "happy": "😄", "sad": "😢", "angry": "😠",
    "surprise": "😲", "fear": "😨", "disgust": "🤢", "neutral": "😐"
}


engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_and_transcribe():
    global speech_result, speech_emotion
    model = Model("vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    def callback(indata, frames, time, status):
        nonlocal rec
        if rec.AcceptWaveform(indata):
            result = json.loads(rec.Result())
            if 'text' in result:
                text = result['text']
                if text:
                    speech_result = text
                    blob = TextBlob(text)
                    polarity = blob.sentiment.polarity
                    if polarity > 0.1:
                        speech_emotion = "Positive 😊"
                    elif polarity < -0.1:
                        speech_emotion = "Negative 😟"
                    else:
                        speech_emotion = "Neutral 😐"
                    speak(f"You sound {speech_emotion.split()[0].lower()}")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            time.sleep(0.1)

threading.Thread(target=listen_and_transcribe, daemon=True).start()


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        face_emotion = analysis[0]['dominant_emotion']
        face_confidence = analysis[0]['emotion'][face_emotion]
        face_emotions_counter[face_emotion] += 1
    except:
        face_emotion = "None"
        face_confidence = 0

 
    overlay = f"Face: {face_emotion} {emoji_map.get(face_emotion, '')} ({face_confidence:.1f}%)"
    cv2.putText(frame, overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Speech: {speech_result[-60:]}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Speech Emotion: {speech_emotion}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 100, 255), 2)

    
    y_offset = 130
    for emo, count in face_emotions_counter.most_common(3):
        stat = f"{emo}: {count}"
        cv2.putText(frame, stat, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
        y_offset += 25

    cv2.putText(frame, "Press Q to quit", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)

    cv2.imshow("Multimodal Emotion Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
print("✅ App closed.")
