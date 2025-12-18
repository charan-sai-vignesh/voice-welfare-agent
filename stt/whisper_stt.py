import whisper
import soundfile as sf
import numpy as np

_model = None

def load_model():
    global _model
    if _model is None:
        _model = whisper.load_model("small")
    return _model

def speech_to_text(audio_path):
    model = load_model()

    audio, samplerate = sf.read(audio_path)

    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    result = model.transcribe(
        audio,
        language="te",
        fp16=False,
        temperature=0.0
    )

    return result["text"]
