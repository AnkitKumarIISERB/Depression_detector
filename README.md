# 🧠 Depression Detection App

A multimodal AI-powered desktop application that screens for depression by analyzing both **spoken responses** and **facial emotions** using real-time webcam and microphone input.

---

## 📌 Features

- 🎙️ **Voice-based Questionnaire** — Uses Vosk speech recognition to transcribe spoken answers to 9 standard depression screening questions.
- 🧠 **Facial Emotion Detection** — Uses DeepFace to analyze your facial expressions during responses.
- 📈 **Depression Risk Scoring** — Calculates a depression risk score based on emotional patterns and answer content.
- 🖼️ **Emotion Chart Generation** — Creates a bar chart of detected emotions throughout the session.
- 📄 **Automatic Report PDF** — Generates a summary report with risk score, responses, and chart upon completion.

---

## 📷 App Preview

![Emotion Chart](assets/sample_emotion_chart.png)

*Note: This image is just a placeholder. Real charts and reports are generated dynamically.*

---

## 🛠️ Installation

### 1. Clone the Repository

git clone https://github.com/AnkitKumarIISERB/Depression_detector.git
cd Depression_detector

### 2. Install Requirements

pip install -r requirements.txt

## 📦 Requirements

Python 3.7 or higher
Webcam + Microphone access
OS: Windows, macOS, or Linux

## 🧪 How to Run

### 1. Run the GUI App

python emotion_gui_app.py

The app will display a live webcam feed.
It will ask 9 questions one-by-one using text-to-speech.
You respond verbally; your speech and facial expressions are recorded and analyzed.
After all questions, a PDF report (report.pdf) and an emotion chart (emotion_chart.png) are saved.

### 2. Run the Multimodal Emotion Detector (Live Feed)

python emotion_multimodal.py

This version:
Displays live webcam feed
Tracks face emotion and sentiment from live speech
Displays both in real-time on screen

## 📁 Project Structure

Depression_detector/
│
├── emotion_gui_app.py            # Main GUI assessment application
├── emotion_multimodal.py         # Live emotion + sentiment detector
├── emotion_from_text.py          # Text sentiment test module
├── emotion_from_speech.py        # Speech emotion test module
├── speech_to_text.py             # Voice-to-text helper
├── test_model.py                 # Optional model test
│
├── vosk-model-small-en-us-0.15/  # Vosk model files (unzip if using locally)
├── assets/                       # Charts, icons, and sample visuals
│
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── LICENSE

## ⚠️ Notes

vosk-model-small-en-us-0.15.zip was removed to keep the repo light. Download it manually if needed:
👉 https://alphacephei.com/vosk/models
The app uses real-time webcam and mic — it will not work in restricted environments or virtualized terminals (like some Colab setups).

## 📄 Report Output

After completing the full GUI-based screening, two files will be generated:
report.pdf – Summary with questions, responses, risk score, and recommendation
emotion_chart.png – A bar chart of detected facial emotions

## ✍️ Future Improvements

Add login/user profile support for tracking over time
Deploy using PyInstaller to distribute as a desktop .exe app
Add support for multilingual assessment

## 👨‍💻 Author

Ankit Kumar

## 📜 License

This project is licensed under the MIT License — see LICENSE file for details.


