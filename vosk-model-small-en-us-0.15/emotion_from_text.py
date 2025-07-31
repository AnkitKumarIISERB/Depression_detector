from textblob import TextBlob

# Sample input text (you can replace with your speech-to-text output)
text = input("💬 Enter some text: ")

# Create a TextBlob object
blob = TextBlob(text)

# Get polarity (sentiment score)
polarity = blob.sentiment.polarity

# Decide emotion based on polarity
if polarity > 0.3:
    emotion = "😊 Positive / Happy"
elif polarity < -0.3:
    emotion = "😠 Negative / Angry or Sad"
else:
    emotion = "😐 Neutral / Unclear"

print(f"\n🧠 Emotion detected: {emotion}")
print(f"📊 Sentiment Score: {polarity}")
