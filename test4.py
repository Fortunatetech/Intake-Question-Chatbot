import streamlit as st
import os
import openai
from components.intake_logic import intake_logic
from components.data_validation import (
    validate_name,
    validate_date_of_birth,
    validate_yes_no,
    validate_open_text,
    validate_email,
    validate_phone_number,
)

from components.intake_question_bank import intake_question_generator
from dotenv import load_dotenv
load_dotenv()

os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

# Streamlit app setup
st.title("Patient Form Intake Assistant")

# Initialize session state
if "intake_step" not in st.session_state:
    st.session_state.intake_step = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "is_minor" not in st.session_state:
    st.session_state.is_minor = False
if "ocd_yes_count" not in st.session_state:
    st.session_state.ocd_yes_count = 0

intake_questions = intake_question_generator()

# Helper to validate responses
def validate_response(question_index, user_input):
    """Validate user input based on the current question index."""
    if question_index in [1, 2]:  # Name validation
        return validate_name(user_input), "Please enter a valid name (letters only)."
    elif question_index == 4:  # Date of birth
        return validate_date_of_birth(user_input), "Please enter a valid date in MM/DD/YYYY format."
    elif question_index in [5, 22, 23, 24, 30]:  # Yes/No questions
        return validate_yes_no(user_input), "Please answer 'Yes' or 'No'."
    elif question_index == 18:  # Email validation
        return validate_email(user_input), "Please enter a valid email address."
    elif question_index == 19:  # Phone number
        return validate_phone_number(user_input), "Please enter a valid 10-digit phone number."
    else:  # Default open-text validation
        return validate_open_text(user_input), "This field cannot be empty. Please provide a response."

# Display the current question
def display_question(step):
    """Display the current question."""
    question = intake_questions[step]
    st.chat_message("assistant").markdown(question)
    return question

# Initialize intake process
if st.session_state.intake_step == 0:
    st.chat_message("assistant").markdown(intake_questions[0])
    st.session_state.intake_step += 1

# Handle user input
user_input = st.chat_input("Your response:")

if user_input:
    current_step = st.session_state.intake_step

    # Validate response
    is_valid, error_message = validate_response(current_step, user_input)
    if not is_valid:
        st.error(error_message)
    else:
        # Save valid response
        st.session_state.responses.append(user_input)
        st.chat_message("user").markdown(user_input)

        # Determine next step
        next_step = intake_logic(current_step, user_input)
        if next_step < len(intake_questions):
            # Ask next question
            st.session_state.intake_step = next_step
            display_question(next_step)
        else:
            # Final message
            final_message = "Thank you for completing the intake form. We’ll process your information shortly!"
            st.chat_message("assistant").markdown(final_message)
            st.stop()
