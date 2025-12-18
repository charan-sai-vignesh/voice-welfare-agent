def evaluator(result):
    if not result:
        return {"status": "FAIL", "message": "డేటా అందుబాటులో లేదు"}

    if "schemes" in result and not result["schemes"]:
        return {"status": "FAIL", "message": "మీకు అర్హమైన పథకాలు లేవు"}

    return {"status": "OK"}
