import torchaudio

# Minimal script to check torchaudio functionality
def check_audio_backend():
    backend = torchaudio.get_audio_backend()
    print(f"Current torchaudio backend: {backend}")

    # Path to a local wav file
    local_audio_path = "preamble10.wav"
    audio, sample_rate = torchaudio.load(local_audio_path)
    print(f"Loaded audio with sample rate: {sample_rate}")

check_audio_backend()