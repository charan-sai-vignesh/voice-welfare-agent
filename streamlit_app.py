import streamlit as st
import io
import soundfile as sf

from audio_recorder_streamlit import audio_recorder
from stt.whisper_stt import speech_to_text
from tts.coqui_tts import text_to_speech
from agent.memory import Memory
from agent.main_agent import run_agent


st.set_page_config(page_title="తెలుగు ప్రభుత్వ పథక సహాయకుడు", layout="centered")

st.title("🎙️ తెలుగు ప్రభుత్వ పథక సహాయకుడు")
st.write("మీ వాయిస్‌లో మాట్లాడండి. సమాధానం వాయిస్‌లోనే వస్తుంది.")

if "memory" not in st.session_state:
    st.session_state.memory = Memory()

audio_bytes = audio_recorder(
    text="🎤 మాట్లాడండి",
    recording_color="#e74c3c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x"
)

if audio_bytes:
    try:
        audio_buffer = io.BytesIO(audio_bytes)
        data, samplerate = sf.read(audio_buffer)

        if len(data.shape) > 1:
            data = data.mean(axis=1)

        sf.write("input.wav", data, samplerate, subtype="PCM_16")
    except Exception:
        st.error(" ఆడియో సమస్య. మళ్లీ ప్రయత్నించండి.")
        st.stop()

    try:
        user_text = speech_to_text("input.wav")
    except Exception:
        st.error(" వాయిస్ స్పష్టంగా లేదు. మళ్లీ మాట్లాడండి.")
        st.stop()

    response_text = run_agent(user_text, st.session_state.memory)

    text_to_speech(response_text, "output.wav")
    st.audio("output.wav", format="audio/wav")

with st.expander("Agent Debug"):
    st.json(st.session_state.memory.data)
