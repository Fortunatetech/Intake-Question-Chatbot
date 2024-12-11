import streamlit as st
from openai import OpenAI
from components.intake_question_bank import intake_question_generator
from components.data_validation import (
    validate_name, validate_date_of_birth, validate_yes_no, validate_gender,
    validate_address, validate_email, validate_phone_number, validate_open_text,
    validate_checkbox, validate_signature
)

# Load questions
intake_questions = intake_question_generator()

st.title("Patient Form Intake Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "intake_step" not in st.session_state:
    st.session_state.intake_step = 0  # Track which question we're on

if "responses" not in st.session_state:
    st.session_state.responses = []

if "conditional_branching" not in st.session_state:
    st.session_state.conditional_branching = {"is_minor": False, "ocd_yes_count": 0}

# Validation Function Wrapper
def validate_response(question_index, response):
    """Validates the response for the current question."""
    if question_index == 1 or question_index == 2:  # Name validation
        return validate_name(response)
    elif question_index == 3:  # Date of birth validation
        return validate_date_of_birth(response)
    elif question_index == 4:  # Is this appointment for a minor child?
        return validate_yes_no(response)
    elif question_index in [7, 8]:  # Minor child-related validations
        return validate_open_text(response)
    elif question_index == 16:  # Email validation
        return validate_email(response)
    elif question_index == 17:  # Phone number validation
        return validate_phone_number(response)
    elif question_index >= 20 and question_index <= 22:  # OCD-related questions
        return validate_yes_no(response)
    else:
        return validate_open_text(response)

# Navigation Logic
def get_next_step(current_step, response):
    """Determine the next question index based on the response."""
    if current_step == 4:  # Is this appointment for a minor child?
        if response.lower() == "yes":
            st.session_state.conditional_branching["is_minor"] = True
            return current_step + 1  # Go to minor child-specific questions
        else:
            st.session_state.conditional_branching["is_minor"] = False
            return current_step + 5  # Skip minor child questions

    if current_step in [20, 21, 22]:  # OCD-related questions
        if response.lower() == "yes":
            st.session_state.conditional_branching["ocd_yes_count"] += 1

        if current_step == 22:  # After the last OCD question
            if st.session_state.conditional_branching["ocd_yes_count"] >= 2:
                return 23  # Go to specialized OCD treatment question
            else:
                return 24  # Skip to optional ketamine therapy question

    return current_step + 1  # Default: move to the next question

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if there is a current question to ask
if st.session_state.intake_step < len(intake_questions):
    current_question_index = st.session_state.intake_step
    current_question = intake_questions[current_question_index]

    user_input = st.chat_input("Your response:")

    if user_input:
        # Validate the user's response
        if not validate_response(current_question_index, user_input):
            st.error("Invalid response. Please try again.")
        else:
            # Append user response to the conversation
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Save the response
            st.session_state.responses.append(user_input)

            # Determine the next step
            next_step = get_next_step(current_question_index, user_input)

            # Append the bot's next message
            if next_step < len(intake_questions):
                next_question = intake_questions[next_step]
                with st.chat_message("assistant"):
                    st.markdown(next_question)
                st.session_state.messages.append({"role": "assistant", "content": next_question})
            else:
                # Completion message
                final_message = "Thank you for providing your details. We’ll process your information and get back to you shortly!"
                with st.chat_message("assistant"):
                    st.markdown(final_message)
                st.session_state.messages.append({"role": "assistant", "content": final_message})

            # Update the intake step
            st.session_state.intake_step = next_step
else:
    # If all questions are completed, show a final message
    final_message = "Thank you for providing your details. We’ll process your information and get back to you shortly!"
    with st.chat_message("assistant"):
        st.markdown(final_message)
    st.session_state.messages.append({"role": "assistant", "content": final_message})
