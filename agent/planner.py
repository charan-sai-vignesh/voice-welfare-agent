def planner(user_text, memory):
    missing = memory.missing_fields()
    if missing:
        return {
            "action": "ASK_INFO",
            "missing": missing,
            "prompt": f"దయచేసి {missing} వివరాలు చెప్పండి"
        }
    return {"action": "CHECK_ELIGIBILITY"}
