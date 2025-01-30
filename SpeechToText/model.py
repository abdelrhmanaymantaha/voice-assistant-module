import torch
import whisper
import contextlib

@contextlib.contextmanager
def patch_torch_load():
    """Temporarily patch torch.load to use weights_only=True."""
    original_load = torch.load
    torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, weights_only=True)
    try:
        yield
    finally:
        torch.load = original_load

def speech_to_text(source_file):
    # Load the Whisper model with patched torch.load
    with patch_torch_load():
        model = whisper.load_model("small.en")
    
    # Transcribe the audio
    result = model.transcribe(source_file)

    # Return the transcribed text
    return result["text"]

# Example usage
if __name__ == "__main__":
    audio_file = "D:/BFOE/grad__project/voice-assistant/output.wav"  
    transcribed_text = speech_to_text(audio_file)
    print("Transcribed Text:")
    print(transcribed_text)