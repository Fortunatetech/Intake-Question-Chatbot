import streamlit as st
import os
import openai
from components.intake_logic import intake_logic
from components.data_validation import (
    validate_name, validate_date_of_birth, validate_yes_no, validate_open_text
)

from dotenv import load_dotenv
load_dotenv()

os.getenv("OPENAI_API_KEY")
# OpenAI API configuration
openai.api_key = "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"

# Streamlit app setup
st.title("Patient Form Intake Assistant")

# Initialize session state
if "intake_step" not in st.session_state:
    st.session_state.intake_step = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "responses" not in st.session_state:
    st.session_state.responses = []
if "is_minor" not in st.session_state:
    st.session_state.is_minor = False
if "ocd_yes_count" not in st.session_state:
    st.session_state.ocd_yes_count = 0
if "greeting_shown" not in st.session_state:
    st.session_state.greeting_shown = False

# Greeting message
greeting_message = (
    "Hi there! Let’s get started with your intake process. "
    "I’ll ask you some questions to ensure we can provide you with the best care possible. Let’s begin!"
)

# Helper function to get question from OpenAI
def generate_question(step, responses):
    # Provide context to the model
    context = (
        f"You are a friendly virtual assistant helping users complete an intake form. "
        f"The user has already provided the following responses: {responses}. "
        f"Now, you are at step {step}. Ask the next appropriate question in a conversational and friendly manner."
    )
    try:
        # Use OpenAI's Chat API to generate the question
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content 
    except Exception as e:
        st.error(f"Error generating question: {e}")
        return "Could you please repeat that?"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user interaction
user_input = st.chat_input("Your response:")

if user_input:
    if not st.session_state.greeting_shown:
        # First interaction: display greeting message
        st.session_state.greeting_shown = True
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({"role": "assistant", "content": greeting_message})
        with st.chat_message("assistant"):
            st.markdown(greeting_message)
    else:
        # Process subsequent questions
        current_question_index = st.session_state.intake_step
        if current_question_index >= 0:
            # Validate response based on question type
            valid_response = False
            if current_question_index in [1, 2]:
                valid_response = validate_name(user_input)
            elif current_question_index == 4:
                valid_response = validate_date_of_birth(user_input)
            elif current_question_index in [5, 22, 23, 24, 30]:
                valid_response = validate_yes_no(user_input)
            else:
                valid_response = validate_open_text(user_input)

            if not valid_response:
                st.error("Invalid response. Please try again.")
            else:
                # Store user response
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.responses.append(user_input)
                with st.chat_message("user"):
                    st.markdown(user_input)

                # Determine next question step
                next_step = intake_logic(current_question_index, user_input)

                # Generate next question using OpenAI
                if next_step < len(st.session_state.responses) + 1:  # Ensure valid step
                    next_question = generate_question(next_step, st.session_state.responses)
                    st.session_state.messages.append({"role": "assistant", "content": next_question})
                    with st.chat_message("assistant"):
                        st.markdown(next_question)
                else:
                    final_message = "Thank you for completing the intake form. We’ll process your information shortly!"
                    st.session_state.messages.append({"role": "assistant", "content": final_message})
                    with st.chat_message("assistant"):
                        st.markdown(final_message)

                st.session_state.intake_step = next_step
