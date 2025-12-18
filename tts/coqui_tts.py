from TTS.api import TTS
import os

_tts = None

def load_tts():
    global _tts
    if _tts is None:
        _tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
    return _tts

def text_to_speech(text, output_path):
    tts = load_tts()

    tts.tts_to_file(
        text=text,
        language="te",
        speaker_wav=None,
        file_path=output_path
    )

    if not os.path.exists(output_path) or os.path.getsize(output_path) < 1000:
        raise RuntimeError("TTS failed to generate audio")
