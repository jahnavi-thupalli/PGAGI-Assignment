import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import prompts
import utils

load_dotenv()
MODEL_ID = "llama-3.1-8b-instant"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="TalentScout AI", page_icon="🛡️")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm TalentScout AI. To begin, may I have your full name?"}]
if "step" not in st.session_state:
    st.session_state.step = 0
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0

st.title("TalentScout Hiring Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("Type your response here..."):

    if utils.check_exit_keyword(user_input):
        st.session_state.messages.append({"role": "user", "content": user_input})
        farewell = "Thank you for your time. Your application has been logged. Goodbye!"
        st.session_state.messages.append({"role": "assistant", "content": farewell})
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    with st.chat_message("assistant"):
        if st.session_state.step < 6:
            keys = ["full_name", "email", "phone", "years_experience", "desired_position", "location"]
            next_prompts = ["What is your email address?", "Your phone number?", "Years of experience?", "Desired position?", "Current location?", "Finally, what is your Tech Stack?"]

            is_valid = True
            if st.session_state.step == 1 and not utils.validate_email(user_input):
                bot_resp = "That doesn't look like a valid email. Please try again."
                is_valid = False
            elif st.session_state.step == 2 and not utils.validate_phone(user_input):
                bot_resp = "Please enter a valid phone number."
                is_valid = False

            if is_valid:
                st.session_state.candidate_data[keys[st.session_state.step]] = user_input
                bot_resp = next_prompts[st.session_state.step]
                st.session_state.step += 1

            st.markdown(bot_resp)
            st.session_state.messages.append({"role": "assistant", "content": bot_resp})

        elif st.session_state.step == 6:
            st.session_state.candidate_data["tech_stack"] = user_input
            with st.spinner("Preparing your technical screening..."):
                try:
                    p = prompts.generate_questions_prompt(
                        user_input,
                        st.session_state.candidate_data.get("years_experience", "N/A"),
                        st.session_state.candidate_data.get("desired_position", "N/A")
                    )

                    completion = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[{"role": "system", "content": prompts.SYSTEM_PROMPT}, {"role": "user", "content": p}]
                    )

                    raw_text = completion.choices[0].message.content
                    qs = [q.replace("Q:", "").strip() for q in raw_text.split("\n") if "Q:" in q]

                    if not qs:
                        qs = [line.strip() for line in raw_text.split('\n') if len(line.strip()) > 10][:5]

                    st.session_state.tech_questions = qs
                    utils.save_candidate_data(st.session_state.candidate_data)

                    bot_resp = f"Acknowledge: {user_input}. Let's begin the interview.\n\n**Question 1:** {st.session_state.tech_questions[0]}"
                    st.session_state.step = 7
                except Exception as e:
                    bot_resp = f"I encountered an error generating questions: {e}. Let's try again."

            st.markdown(bot_resp)
            st.session_state.messages.append({"role": "assistant", "content": bot_resp})

        elif st.session_state.step == 7:
            st.session_state.current_q_idx += 1

            if st.session_state.current_q_idx < len(st.session_state.tech_questions):
                q_text = st.session_state.tech_questions[st.session_state.current_q_idx]
                bot_resp = f"**Question {st.session_state.current_q_idx + 1}:** {q_text}"
            else:
                bot_resp = "Interview complete! Thank you for sharing your expertise. Our team will review your application and be in touch. Goodbye!"
                st.session_state.step = 8 # Final State

            st.markdown(bot_resp)
            st.session_state.messages.append({"role": "assistant", "content": bot_resp})
