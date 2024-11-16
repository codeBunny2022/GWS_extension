import speech_recognition as sr
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Load translation models
translation_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translation_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translator = pipeline("translation_en_to_ru", model=translation_model, tokenizer=translation_tokenizer)

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    # Set up the response
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

# Main function to process audio input and perform translation
def main():
    microphone = sr.Microphone()

    while True:
        print("Say something!")
        response = recognize_speech_from_mic(recognizer, microphone)

        if response["success"]:
            english_text = response["transcription"]
            print(f"English Text: {english_text}")

            # Translate English text to Russian
            translated_text = translator(english_text)[0]['translation_text']
            print(f"Translated Text (Russian): {translated_text}")

        if not response["success"]:
            print(f"Error: {response['error']}")

        # Adding a simple mechanism to break the loop
            print("Exiting...")
            break
        if response["success"] and english_text.lower() in ["exit", "quit", "stop"]:

if __name__ == "__main__":
    main()