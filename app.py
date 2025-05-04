# save this as app.py
from flask import Flask, request, jsonify
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file temporarily
    filepath = os.path.join('temp_audio', file.filename)
    os.makedirs('temp_audio', exist_ok=True)
    file.save(filepath)

    # Recognize the audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        os.remove(filepath)  # Clean up
        return jsonify({'text': text})
    except sr.UnknownValueError:
        os.remove(filepath)
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        os.remove(filepath)
        return jsonify({'error': f'Error from Google API: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
