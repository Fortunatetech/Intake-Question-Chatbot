from components.intake_question_bank import intake_question_generator
from components.data_validation import validate_yes_no, validate_open_text
import streamlit as st

intake_questions = intake_question_generator()


def intake_logic(current_question_index, response):
    """
    Handles navigation logic based on the current question and user response.
    Args:
        current_question_index (int): Index of the current question in the intake questions list.
        response (str): User response to the current question.

    Returns:
        next_question_index (int): The index of the next question to ask.
    """
    # Branching for "Is this appointment for a minor child?"
    if current_question_index == 5:  # Question index for minor child
        if validate_yes_no(response) and response.lower() == "yes":
            st.session_state.is_minor = True
            return 6  # Go to the next minor child-specific question
        else:
            st.session_state.is_minor = False
            return 10  # Skip to "sex assigned at birth"

    # OCD-related questions (indices: 22, 23, 24)
    if current_question_index in [22, 23, 24]:
        if validate_yes_no(response) and response.lower() == "yes":
            st.session_state.ocd_yes_count += 1

        if current_question_index == 24:  # Last OCD question
            if st.session_state.ocd_yes_count >= 2:
                return 25  # Go to specialized OCD treatment question
            else:
                return 26  # Skip to optional therapy offer

    # "Do you have current thoughts of self-harm or harming others?"
    if current_question_index == 30:
        if validate_yes_no(response) and response.lower() == "yes":
            return 31  # Follow-up self-harm question
        else:
            return 32  # Proceed to "Personal Life"

    # General case: move to the next question
    return current_question_index + 1
