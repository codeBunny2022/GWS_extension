import speech_recognition as sr
from googletrans import Translator

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error with the request: ", e)

# Function to translate text
def translate_text(text, dest_language='fr'):
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

# Main function
def main():
    dest_language = input("Please enter the target language code (e.g., 'fr' for French, 'es' for Spanish): ")

    while True:
        text = recognize_speech()
        if text:
            translated_text = translate_text(text, dest_language)
            if translated_text:
                print(f"Translated: {translated_text}")
        command = input("Press 'q' to quit or any other key to continue: ")
        if command.lower() == 'q':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()