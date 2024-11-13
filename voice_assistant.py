import torchaudio
import requests
from transformers import AutoProcessor, SeamlessM4TModel

# Set backend, if necessary torchaudio.set_audio_backend("soundfile") - but as per warning remove this
# Removing it since dispatcher finds backend automatically, and the warning says it's a no-op anyway

# Load the processor and model
processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

# Define the audio file URL and local path
audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/preamble10.wav"
local_audio_path = "preamble10.wav"

# Download the audio file
response = requests.get(audio_url)
with open(local_audio_path, 'wb') as f:
    f.write(response.content)

# Read the downloaded audio file and resample to 16kHz
audio, original_sample_rate = torchaudio.load(local_audio_path)
audio = torchaudio.functional.resample(audio, orig_freq=original_sample_rate, new_freq=16000)  # Resampling to 16kHz

# Process the audio with the processor
audio_inputs = processor(audio, sampling_rate=16000, return_tensors="pt")

# Process some input text for comparison
text_inputs = processor(text="Hello, my dog is cute", src_lang="eng", return_tensors="pt")

# Generate audio from text
generated_audio_from_text = model.generate(**text_inputs, tgt_lang="rus").squeeze().cpu().numpy()

# Generate translated text from audio (speech-to-text)
output_tokens_from_audio = model.generate(**audio_inputs, tgt_lang="fra", generate_speech=False)
translated_text_from_audio = processor.batch_decode(output_tokens_from_audio, skip_special_tokens=True)[0]

# Generate translated text from text (text-to-text)
output_tokens_from_text = model.generate(**text_inputs, tgt_lang="fra", generate_speech=False)
translated_text_from_text = processor.batch_decode(output_tokens_from_text, skip_special_tokens=True)[0]

print("Generated Audio from Text:", generated_audio_from_text)
print("Translated Text from Audio:", translated_text_from_audio)
print("Translated Text from Text:", translated_text_from_text)