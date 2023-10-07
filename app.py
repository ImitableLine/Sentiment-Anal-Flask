from flask import Flask, request, render_template, jsonify
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
app = Flask(__name__)

# Load the Keras model
model = tf.keras.models.load_model("models/sentiment_modelALPHA.h5")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['twitter_link']

        # Load the tokenizer from the saved file
        with open('models/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        sequences = tokenizer.texts_to_sequences([user_input])  # Wrap user_input in a list
        padded_sequences = pad_sequences(sequences, maxlen=49, padding='post')
        prediction = model.predict(padded_sequences)

        # Assuming the model outputs a probability, you can determine the sentiment based on a threshold.
        # Apply the threshold to each prediction value in the array
        sentiments = ["Positive" if p > 0.5 else "Negative" for p in prediction]

        # Convert the prediction array to a regular Python list of floats
        confidence = prediction.tolist()[0]

        # Create a response to send back to the user
        response = {
            "user_input": user_input,
            "sentiment": sentiments,
            "confidence": confidence  # Convert to list of floats
        }

        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)