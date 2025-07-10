import streamlit as st
import requests
import base64
from PIL import Image

# inject custom CSS
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
        }
        .stApp {
            background: radial-gradient(circle at top left, #0d1117, #000000);
            color: white;
        }
        h1 {
            color: #58a6ff;
        }
        .stTextInput, .stSelectbox, .stButton button {
            background-color: #161b22;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


try:
    with open("ai_bot.png", "rb") as img_file:
        img_bytes = img_file.read()
        encoded = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <div style='display: flex; justify-content: center; align-items: center;'>
            <img src='data:image/png;base64,{encoded}' width='130' style='margin-bottom: 10px;'/>
        </div>
        """,
        unsafe_allow_html=True
    )
except:
    st.warning("Image 'ai_bot.png' not found. Please make sure it's in the same directory.")


# title
st.markdown("""
    <h1 style='text-align: center; font-size: 32px; color: #58a6ff; font-family: "Segoe UI", sans-serif; margin-bottom: 10px;'>
        ✧°. ⋆༺ Domain-Specific Chatbot ༻⋆. °✧
    </h1>
""", unsafe_allow_html=True)

# UI elements
model = st.selectbox("Choose a Model", ["gemma3", "tinyllama", "qwen3:0.6b"])
domain = st.selectbox("Choose a Domain", ["Science", "IT", "Medical", "Arts"])
user_input = st.text_input("Ask a question")


# prompt and response
# warn user if model is small
if model == "tinyllama":
    st.caption("⚠️ tinyllama is a smaller model. Responses may be less structured or informative.")

# handle query
if st.button("Ask") and user_input.strip():
    
    # simplified prompt for smaller models
    if model == "tinyllama":
        prompt = f"""
        You are an expert in {domain}. Only answer questions related to this domain.
        Be brief, accurate, and avoid speculation. If the question is off-topic, politely decline.

        Question: {user_input}
        Answer:
        """

    elif model == "qwen3:0.6b":
        prompt = (
            f"You are a professional assistant that only answers questions related to the domain: **{domain}**.\n"
            f"Your instructions:\n"
            f"- If the question is related to **{domain}**, give a short, factual, and clear answer.\n"
            f"- If the question is NOT related to **{domain}**, respond ONLY with:\n"
            f'  "Sorry, I can only answer questions related to {domain}."\n'
            f"- Do NOT add any extra thoughts, explanations, or guesses.\n"
            f"- Do NOT include '<think>' or internal thoughts.\n\n"
            f"Examples:\n"
            f"Q: What is the capital of France?\n"
            f"A: Sorry, I can only answer questions related to {domain}.\n\n"
            f"Q: Who painted the Mona Lisa?\n"
            f"A: Leonardo da Vinci.\n\n"
            f"Q: {user_input}\n"
            f"A:"
        )

    
    # full structured prompt for better models
    else:
        prompt = f"""
            System:
            You are a domain-expert assistant specialized in **{domain}**, operating as a world-class professional with rigorous adherence to factual accuracy, domain compliance, and ethical safety.
            You must:
            1. **Accept only questions strictly within {domain}.** If the user asks something outside the domain, politely decline.
            2. **Adhere to domain-specific guardrails**: 
            - Avoid speculation or unverified advice.
            - Cite sources or state "I don't know" if data isn't available.
            - Respect any legal, medical, or compliance boundaries in {domain}.
            3. **Use a structured reasoning approach**:
            - Step 1: Clarify ambiguous terms, if needed.
            - Step 2: Apply domain knowledge with concise, accurate detail.
            - Step 3: Summarize findings and suggest next steps or referrals.
            4. **Format output clearly**: use headings, bullet points, and citations.

            Example:
            User: “What's the latest breakthrough in {domain}?”
            Assistant:
            - **Step 1 - Clarification**: “Do you mean recent peer-reviewed studies from the past year or industry developments?”
            - **Step 2 - Answer**: “A 2025 study in Journal X showed… [citation].”
            - **Step 3 - Summary & Next Steps**: “In summary… For deeper exploration, see article Y.”

            User: {user_input}
            Assistant:
            """


    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()

        if 'response' in data:
            st.markdown(f"**Response:** {data['response']}")
        else:
            st.error("No 'response' key found in the model output:")
            st.json(data)
    except Exception as e:
        st.error(f"Something went wrong: {e}")