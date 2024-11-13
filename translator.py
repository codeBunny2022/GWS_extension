import torchaudio
import requests
import torch
from transformers import AutoProcessor, SeamlessM4TModel

# Load the processor and model
processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

# English text to be translated to Russian and converted to audio
english_text = "I love you"

# Process the English text
text_inputs = processor(text=english_text, src_lang="eng", return_tensors="pt")

# Generate Russian audio from the English text
output = model.generate(**text_inputs, tgt_lang="rus", generate_speech=True)

# since output is probably a tuple, let's inspect its content
print(type(output), len(output))  # Inspects the type and structure of the output

if isinstance(output, tuple):
    generated_audio_from_text = output[0]  # Access the actual audio tensor
    generated_audio_from_text = generated_audio_from_text.squeeze().cpu().numpy()

    # Convert the 1D numpy array to a 2D tensor as expected by torchaudio.save
    generated_audio_tensor = torch.tensor(generated_audio_from_text).unsqueeze(0)

    # Save the generated audio to a WAV file
    torchaudio.save("output_russian_audio.wav", generated_audio_tensor, 16000)

    print("Russian Audio Generated and saved as 'output_russian_audio.wav'")
else:
    print("Unexpected output format:", output)