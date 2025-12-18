import streamlit as st
import io
import numpy as np
import soundfile as sf
import os

from audio_recorder_streamlit import audio_recorder
from stt.whisper_stt import speech_to_text
from tts.coqui_tts import text_to_speech
from agent.memory import Memory
from agent.main_agent import run_agent


st.set_page_config(page_title="తెలుగు ప్రభుత్వ పథక సహాయకుడు")

st.title("🎙️ తెలుగు ప్రభుత్వ పథక సహాయకుడు")
st.write("మైక్ నొక్కి 4–5 సెకండ్లు స్పష్టంగా మాట్లాడండి.")

if "memory" not in st.session_state:
    st.session_state.memory = Memory()

audio_bytes = audio_recorder(
    text="🎤 మాట్లాడండి",
    recording_color="#e74c3c",
    neutral_color="#6aa36f"
)

if audio_bytes:

    audio_buffer = io.BytesIO(audio_bytes)
    data, samplerate = sf.read(audio_buffer)

    if len(data.shape) > 1:
        data = data.mean(axis=1)

    duration = len(data) / samplerate
    energy = float(np.mean(np.abs(data)))

    if duration < 1.5 or energy < 0.003:
        st.error(" వాయిస్ స్పష్టంగా లేదు. మైక్ దగ్గరగా మాట్లాడండి.")
        st.stop()

    sf.write("input.wav", data, samplerate, subtype="PCM_16")

    user_text = speech_to_text("input.wav")

    if user_text.strip() == "":
        st.error(" వాయిస్ అర్థం కాలేదు. మళ్లీ ప్రయత్నించండి.")
        st.stop()

    response_text = run_agent(user_text, st.session_state.memory)

    text_to_speech(response_text, "output.wav")

    if not os.path.exists("output.wav"):
        st.error(" వాయిస్ తయారు కాలేదు (TTS సమస్య)")
        st.stop()

    st.audio("output.wav", format="audio/wav")

