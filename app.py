import streamlit as st
import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# Resume parser
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Gemini response
def ask_gemini(resume_text, user_query):
    prompt = f"""
You are an expert career advisor AI.

Here is a user's resume:
{resume_text}

The user asked: "{user_query}"

Please provide a detailed, structured, and professional answer based on the resume and question.
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Recruiter Chatbot | myjobb.ai", layout="centered")
st.title("🤖 Recruiter Chatbot - myjobb.ai MVP")

st.markdown("Upload your resume and ask a career-related question. Gemini will guide you!")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])
user_query = st.text_input("💬 Enter your question (e.g., 'What roles suit me?')")

if st.button("Get Advice"):
    if not uploaded_file or not user_query:
        st.warning("Please upload a resume and enter a question.")
    else:
        with st.spinner("Processing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            response = ask_gemini(resume_text, user_query)

        st.success("Here's your personalized advice:")
        st.markdown(response)
