import re
import json
import os
import validators

def validate_email(email):
    return validators.email(email) # Validates format of the e-Mail

def validate_phone(phone):
    pattern = r"^\+?[1-9]\d{1,14}$|^(\d{3}-\d{3}-\d{4})$|^\d{10}$"
    return bool(re.match(pattern, phone.replace(" ", "")))

def save_candidate_data(candidate_info, filename="candidates.json"):
    data = []

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(candidate_info)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return True

def check_exit_keyword(user_input):
    exit_keywords = ["exit", "quit", "bye", "terminate", "goodbye", "thank you", "end"]
    return any(word in user_input.lower() for word in exit_keywords)
