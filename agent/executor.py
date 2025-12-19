from tools.eligibility_engine import check_eligibility
from tools.scheme_retriever import retrieve_scheme
from tools.mock_gov_api import submit_application

def executor(plan, memory):
    action = plan.get("action")

    if action == "CHECK_ELIGIBILITY":
        schemes = check_eligibility(memory.data)
        return {"schemes": schemes}

    if action == "RETRIEVE_SCHEME":
        return retrieve_scheme(plan["scheme"])

    if action == "APPLY":
        return submit_application(memory.data)

    
    return {"status": "NO_ACTION", "reason": f"Unsupported action: {action}"}
