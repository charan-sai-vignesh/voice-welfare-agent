def check_eligibility(user):
    schemes = []

    if user["occupation"] == "farmer" and user["income"] < 200000:
        schemes.append("రైతు భరోసా")

    if user["age"] >= 60:
        schemes.append("వృద్ధాప్య పింఛన్")

    return schemes
