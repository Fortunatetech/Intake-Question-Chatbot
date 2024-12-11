import re

def validate_name(name):
    """Validate a name (only alphabetic characters allowed)."""
    return bool(re.match(r"^[A-Za-z\s\-]+$", name))

def validate_date_of_birth(dob):
    """Validate the date format MM/DD/YYYY."""
    return bool(re.match(r"^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$", dob))

def validate_yes_no(response):
    """Validate Yes/No responses."""
    return response.lower() in ["yes", "no"]

def validate_gender(response):
    """Validate gender selection."""
    return response.lower() in ["male", "female", "other"]

def validate_address(address):
    """Validate address (basic check for non-empty)."""
    return len(address.strip()) > 0

def validate_email(email):
    """Validate email format."""
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def validate_phone_number(phone):
    """Validate phone number (basic format check for 10 digits)."""
    return bool(re.match(r"^\d{10}$", phone))

def validate_open_text(response):
    """Validate free-text responses (ensure not empty)."""
    return len(response.strip()) > 0

def validate_checkbox(response, options):
    """Validate checkbox selections (response must be in options)."""
    return response.lower() in [option.lower() for option in options]

def validate_signature(signature):
    """Validate signature (non-empty name-like input)."""
    return validate_name(signature)