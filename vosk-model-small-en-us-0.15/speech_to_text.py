import queue
import sounddevice as sd
import vosk
import json

# Create a queue to hold audio chunks
q = queue.Queue()

# Load your model
model = vosk.Model("vosk-model-small-en-us-0.15")

# Callback to feed mic input into the queue
def callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    q.put(bytes(indata))

# Set sample rate and duration
samplerate = 16000
duration = 5  # seconds to record

# Start recording
print("🎤 Speak now...")

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)

    for _ in range(int(samplerate / 8000 * duration)):
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("📝 You said:", result.get("text"))

    final = json.loads(rec.FinalResult())
    print("✅ Final output:", final.get("text"))
