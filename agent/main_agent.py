from agent.planner import planner
from agent.executor import executor
from agent.evaluator import evaluator

def run_agent(user_text, memory):
    plan = planner(user_text, memory)
    result = executor(plan, memory)
    evaluation = evaluator(result)

    if evaluation["status"] != "OK":
        return evaluation["message"]

    return f"మీకు అర్హమైన పథకాలు: {result['schemes']}"
