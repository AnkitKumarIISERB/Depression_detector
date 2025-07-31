import queue
import sounddevice as sd
import vosk
import json
from textblob import TextBlob

# 1. Setup audio queue
q = queue.Queue()

# 2. Load Vosk model
from vosk import Model
model = Model("vosk-model-small-en-us-0.15")

# 3. Define callback for mic input
def callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    q.put(bytes(indata))

# 4. Start listening
samplerate = 16000
duration = 5  # seconds

print("🎤 Speak now...")

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)

    for _ in range(int(samplerate / 8000 * duration)):
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text")
            if text:
                print(f"📝 You said: {text}")

                # 🔍 Emotion detection
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity

                if polarity > 0.3:
                    emotion = "😊 Positive / Happy"
                elif polarity < -0.3:
                    emotion = "😠 Negative / Angry or Sad"
                else:
                    emotion = "😐 Neutral / Unclear"

                print(f"🧠 Emotion detected: {emotion}")
                print(f"📊 Sentiment Score: {polarity:.2f}\n")

    # Final output
    final = json.loads(rec.FinalResult())
    print("✅ Final recognized text:", final.get("text"))
