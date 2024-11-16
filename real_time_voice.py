import speech_recognition as sr
import requests

# Initialize recognizer
recognizer = sr.Recognizer()

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
        return None

# Function to translate text using the Seamless API
def translate_text(text, dest_language='fr'):
    api_url = "https://api.seamless.com/translate"
    api_token = "YOUR_SEAMLESS_API_TOKEN" # Replace with your Seamless API token

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_lang": dest_language
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        translation_data = response.json()
        translation = translation_data['translated_text']  # Adjust based on Seamless API's response format
        return translation
    except requests.exceptions.RequestException as e:
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
            else:
                print("Failed to translate text.")
        else:
            print("No text recognized.")
        command = input("Press 'q' to quit or any other key to continue: ")
        if command.lower() == 'q':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()