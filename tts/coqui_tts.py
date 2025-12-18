import asyncio
import edge_tts

VOICE = "te-IN-ShrutiNeural"   # Telugu voice

async def _tts(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def text_to_speech(text, output_path="output.wav"):
    asyncio.run(_tts(text, output_path))

