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

class SpeechToTextPipeline:
    def __init__(self, model_name="small.en"):
        """Initialize the Whisper model as a pipeline."""
        with patch_torch_load():
            self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path):
        """Transcribe an audio file and return text."""
        result = self.model.transcribe(audio_path)
        return result["text"]

# Example usage
if __name__ == "__main__":
    pipeline = SpeechToTextPipeline()  # Load the model once
    audio_file = "D:/BFOE/grad__project/voice-assistant/output.wav"
    
    transcribed_text = pipeline.transcribe(audio_file)
    print("Transcribed Text:", transcribed_text)
