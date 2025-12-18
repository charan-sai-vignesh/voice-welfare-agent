from stt.whisper_stt import speech_to_text
from tts.coqui_tts import text_to_speech
from agent.memory import Memory
from agent.planner import planner
from agent.executor import executor
from agent.evaluator import evaluator

memory = Memory()

def run_agent(audio_input):
    user_text = speech_to_text(audio_input)

    # Simple info extraction (demo)
    if "రైతు" in user_text:
        memory.update("occupation", "farmer")
    if "వయసు" in user_text:
        memory.update("age", 45)
    if "ఆదాయం" in user_text:
        memory.update("income", 150000)

    plan = planner(user_text, memory)

    if plan["action"] == "ASK_INFO":
        response = f"దయచేసి {plan['missing']} వివరాలు చెప్పండి"
        text_to_speech(response)
        return

    result = executor(plan, memory)
    evaluation = evaluator(result)

    if evaluation["status"] == "OK":
        text_to_speech(f"మీకు అర్హమైన పథకాలు: {result['schemes']}")
