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

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "intake_step" not in st.session_state:
    st.session_state.intake_step = 0  # Track which question we're on

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if there is a current question to ask
if st.session_state.intake_step < len(intake_questions):
    if prompt := st.chat_input("Your response:"):
        # Append user response to the conversation
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Append bot's next message
        bot_message = ""
        if st.session_state.intake_step == 0:  # Initial message doesn't need a response
            bot_message = intake_questions[st.session_state.intake_step]
        else:
            bot_message = intake_questions[st.session_state.intake_step]
        
        with st.chat_message("assistant"):
            st.markdown(bot_message)

        st.session_state.messages.append({"role": "assistant", "content": bot_message})
        st.session_state.intake_step += 1
else:
    # Completion message
    final_message = "Thank you for providing your details. We’ll process your information and get back to you shortly!"
    with st.chat_message("assistant"):
        st.markdown(final_message)
    st.session_state.messages.append({"role": "assistant", "content": final_message})

