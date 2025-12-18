def retrieve_scheme(scheme_name):
    schemes = {
        "రైతు భరోసా": "ఈ పథకం రైతులకు ఆర్థిక సహాయం అందిస్తుంది.",
        "వృద్ధాప్య పింఛన్": "60 ఏళ్లు పైబడిన వారికి నెలవారీ పింఛన్."
    }
    return schemes.get(scheme_name, "వివరాలు లభ్యం కావు")
