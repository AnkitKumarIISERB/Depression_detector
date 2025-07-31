import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 5  # Duration

print("🎙️ Recording for 5 seconds...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
write("mic_test.wav", fs, recording)
print("✅ Done! File saved as 'mic_test.wav'")
