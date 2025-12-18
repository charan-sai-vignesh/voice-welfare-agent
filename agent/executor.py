from tools.eligibility_engine import check_eligibility
from tools.scheme_retriever import retrieve_scheme
from tools.mock_gov_api import submit_application

def executor(plan, memory):
    if plan["action"] == "CHECK_ELIGIBILITY":
        schemes = check_eligibility(memory.data)
        return {"schemes": schemes}

    if plan["action"] == "RETRIEVE_SCHEME":
        return retrieve_scheme(plan["scheme"])

    if plan["action"] == "APPLY":
        return submit_application(memory.data)
