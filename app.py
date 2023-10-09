from flask import Flask, request, render_template, jsonify
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from youtubeapi import get_video_comments 

import os
import googleapiclient.discovery

app = Flask(__name__)

# Load the Keras model
model = tf.keras.models.load_model("models/sentiment_modelBETA.h5")
# Load the tokenizer from the saved file
with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['twitter_link']

        sequences = tokenizer.texts_to_sequences([user_input])  # Wrap user_input in a list
        padded_sequences = pad_sequences(sequences, maxlen=49, padding='post')
        prediction = model.predict(padded_sequences)

        # Assuming the model outputs a probability, you can determine the sentiment based on a threshold.
        # Apply the threshold to each prediction value in the array
        sentiments = ["Positive" if p > 0.5 else "Negative" for p in prediction]

        # Convert the prediction array to a regular Python list of floats
        confidence = prediction.tolist()[0]

        # Create a list of prediction objects
        predictions = []
        for i in range(len(sentiments)):
            prediction_obj = {
                "comment": user_input,
                "sentiment": sentiments[i],
                "confidence": confidence[i]  # Convert to list of floats
            }
            predictions.append(prediction_obj)

        # Create a response to send back to the user
        response = {
            "predictions": predictions
        }

        return jsonify(response)


import re

def extract_video_id(url):
    # Regular expression to match the video ID in a YouTube URL
    pattern = r"(v=|vi=|youtu.be/|/embed/|/v/|/e/|watch\?v=|embed/)([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    if match:
        return match.group(2)  # The video ID is in the second group
    else:
        return None

@app.route('/predict_youtube', methods=['POST'])
def predict_youtube():
    if request.method == 'POST':
        # Get video URL and YouTube API key from the form
        video_url = request.form['video_url']
        youtube_api_key = request.form['youtube_api_key']

        # Extract video ID from the URL
        video_id = extract_video_id(video_url)

        # Use the user-entered API key for the YouTube API call
        API_KEY = youtube_api_key

        # Initialize the YouTube Data API client
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

        # Get comments from the video
        comments = get_video_comments(video_id, max_results=3, api_key=youtube_api_key)


        # Perform sentiment analysis on the comments
        sentiments = []

        for comment in comments:
            sequences = tokenizer.texts_to_sequences([comment])  # Wrap comment in a list
            padded_sequences = pad_sequences(sequences, maxlen=49, padding='post')
            prediction = model.predict(padded_sequences)[0]

            # Determine sentiment based on a threshold
            sentiment = "Positive" if prediction > 0.5 else "Negative"

            # Convert the prediction to a regular Python float
            prediction = float(prediction)

            sentiments.append({
                "comment": comment,
                "sentiment": sentiment,
                "confidence": prediction  # Replace with the actual confidence value
            })

        # Create a response to send back to the user
        response = {
            "video_url": video_url,
            "predictions": sentiments
        }

        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)