from flask import Flask, request, jsonify, render_template, send_file
import speech_recognition as sr
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from pydub import AudioSegment
import os
from werkzeug.utils import secure_filename
from gtts import gTTS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Load translation model
translation_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translation_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translator = pipeline("translation_en_to_ru", model=translation_model, tokenizer=translation_tokenizer)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Translate route
@app.route('/translate', methods=['POST'])
def translate():
    src_lang = request.form['src_lang']

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file in request"}), 400

    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(filepath)

    wav_filepath = os.path.splitext(filepath)[0] + '.wav'

    # Convert WebM to WAV using pydub
    sound = AudioSegment.from_file(filepath)
    sound.export(wav_filepath, format="wav")

    with sr.AudioFile(wav_filepath) as source:
        audio_data = recognizer.record(source)

    try:
        english_text = recognizer.recognize_google(audio_data, language=src_lang)
    except sr.RequestError:
        return jsonify({"error": "API unavailable"}), 500
    except sr.UnknownValueError:
        return jsonify({"error": "Unable to recognize speech"}), 400
    finally:
        os.remove(filepath)
        os.remove(wav_filepath)

    translated_text = translator(english_text)[0]['translation_text']

    # Text-to-speech conversion for translated text
    tts = gTTS(text=translated_text, lang='ru')
    tts_audio_path = os.path.join(UPLOAD_FOLDER, 'translated_audio.mp3')
    tts.save(tts_audio_path)

    return jsonify({
        "english_text": english_text,
        "translated_text": translated_text,
        "audio_path": tts_audio_path
    })

# Download audio route
@app.route('/download_audio/<filename>')
def download_audio(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)