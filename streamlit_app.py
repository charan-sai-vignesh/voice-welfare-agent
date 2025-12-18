import streamlit as st
import numpy as np
import scipy.io.wavfile as wavfile
import os

from audio_recorder_streamlit import audio_recorder

from stt.whisper_stt import speech_to_text
from tts.coqui_tts import text_to_speech
from agent.memory import Memory
from agent.main_agent import run_agent


# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="తెలుగు ప్రభుత్వ పథక సహాయకుడు",
    layout="centered"
)

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

    # Save input audio
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
    wavfile.write("input.wav", 44100, audio_np)

    st.success(" వాయిస్ అందుకుంది")

  
    with st.spinner(" వాయిస్ అర్థం చేసుకుంటోంది..."):
        user_text = speech_to_text("input.wav")

   
    with st.spinner(" నిర్ణయం తీసుకుంటోంది..."):
        response_text = run_agent(user_text, st.session_state.memory)

    
    with st.spinner("🔊 సమాధానం తయారవుతోంది..."):
        text_to_speech(response_text, "output.wav")

 
    st.audio("output.wav", format="audio/wav")


# Optional Debug Panel (Evaluator-Friendly)

with st.expander(" Agent Debug (Evaluator View)"):
    st.write(" Memory State")
    st.json(st.session_state.memory.data)
