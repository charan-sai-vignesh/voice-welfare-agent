from agent.planner import planner
from agent.executor import executor
from agent.evaluator import evaluator
import re


def _extract_number_from_text(text: str) -> int:
    """Extract numeric value from Telugu text (handles numbers in words or digits)"""
    
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    
   
    telugu_numbers = {
        "ఐదు": 5, "పది": 10, "పదిహేను": 15, "ఇరవై": 20, "ముప్పై": 30,
        "నలభై": 40, "యాభై": 50, "అరవై": 60, "డెబ్బై": 70, "ఎనభై": 80,
        "తొంభై": 90, "వంద": 100, "వేయి": 1000, "లక్ష": 100000
    }
    
    for word, num in telugu_numbers.items():
        if word in text:
            
            if "లక్ష" in text:
                return 100000
            elif "వేయి" in text:
                return 1000
            return num
    
    return None


def _update_memory_from_text(user_text: str, memory) -> None:
    """
    Extract and update memory from user text in Telugu.
    More flexible extraction to handle variations in speech recognition.
    """
    user_text_lower = user_text.lower()
    
   
    occupation_keywords = {
        "farmer": ["రైతు", "రైతును", "రైతులు", "వ్యవసాయ", "కృషి"],
        "business": ["వ్యాపారి", "వ్యాపార", "వ్యాపారం"],
        "employee": ["ఉద్యోగి", "ఉద్యోగం", "ఉద్యోగ"]
    }
    
    for occ_type, keywords in occupation_keywords.items():
        if any(keyword in user_text for keyword in keywords):
            memory.update("occupation", occ_type)
            break
    
    
    age_keywords = ["వయసు", "ఏళ్ల", "సంవత్సర", "ఏళ్ళ", "వయస్సు", "ఎంత"]
    if any(keyword in user_text for keyword in age_keywords):
        age = _extract_number_from_text(user_text)
        if age and 1 <= age <= 120:
            memory.update("age", age)
        # Also check for common age mentions
        elif "అరవై" in user_text or "60" in user_text:
            memory.update("age", 60)
        elif "నలభై" in user_text or "40" in user_text:
            memory.update("age", 40)
        elif "యాభై" in user_text or "50" in user_text:
            memory.update("age", 50)
    
   
    income_keywords = ["ఆదాయం", "జీతం", "సంపాదన", "ఆదాయ", "జీత", "వేతనం"]
    if any(keyword in user_text for keyword in income_keywords):
        income = _extract_number_from_text(user_text)
        if income:
            
            if "నెల" in user_text or "మాస" in user_text or "నెలకు" in user_text:
                income = income * 12
            
            if "లక్ష" in user_text and income < 1000:
                income = income * 100000
            elif "లక్ష" in user_text:
               
                pass
            memory.update("income", income)
        
        elif "లక్ష" in user_text:
            
            numbers = re.findall(r'\d+', user_text)
            if numbers:
                income = int(numbers[0]) * 100000
                memory.update("income", income)


def run_agent(user_text, memory):
   
    memory_before = memory.data.copy()
    
   
    _update_memory_from_text(user_text, memory)
    
    
    new_info_added = memory.data != memory_before

   
    plan = planner(user_text, memory)

   
    if plan["action"] == "ASK_INFO":
        
        if new_info_added:
            provided = []
            if memory.data["age"] and not memory_before["age"]:
                provided.append(f"వయసు {memory.data['age']}")
            if memory.data["income"] and not memory_before["income"]:
                provided.append(f"ఆదాయం {memory.data['income']}") 
            if memory.data["occupation"] and not memory_before["occupation"]:
                occ_names = {"farmer": "రైతు", "business": "వ్యాపారి", "employee": "ఉద్యోగి"}
                provided.append(occ_names.get(memory.data["occupation"], memory.data["occupation"]))
            
            if provided:
                return f"ధన్యవాదాలు. మీ {', '.join(provided)} వివరాలు నమోదు చేశాను. " + plan["prompt"]
        return plan["prompt"]
    5                                                                        
    
    result = executor(plan, memory)
    evaluation = evaluator(result)

    if evaluation["status"] != "OK":
        return evaluation["message"]

   
    schemes = result.get("schemes", [])
    if schemes:
        schemes_str = ", ".join(schemes)
        return f"మీకు అర్హమైన పథకాలు: {schemes_str}. మరిన్ని వివరాలకు దయచేసి ప్రశ్నించండి."
    else:
        return "ప్రస్తుతం మీకు అర్హమైన పథకాలు లేవు. మరిన్ని సమాచారం అవసరమైతే దయచేసి చెప్పండి."
