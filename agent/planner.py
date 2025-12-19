def planner(user_text, memory):
    missing = memory.missing_fields()
    if missing:
    
        field_names = {
            "age": "వయసు",
            "income": "ఆదాయం",
            "occupation": "వృత్తి"
        }
        missing_telugu = [field_names.get(f, f) for f in missing]
        missing_str = ", ".join(missing_telugu)
        
        return {
            "action": "ASK_INFO",
            "missing": missing,
            "prompt": f"దయచేసి మీ {missing_str} వివరాలు చెప్పండి."
        }
    return {"action": "CHECK_ELIGIBILITY"}
