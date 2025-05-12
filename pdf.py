import os
import fitz  # PyMuPDF for PDF extraction
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="PDF Q&A Chatbot",
    page_icon="📄",
    layout="centered",
)

# Load API Key Securely from Streamlit Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Check if API key is missing
if not GOOGLE_API_KEY:
    st.error("Google API Key is missing! Set it in Streamlit Secrets.")
    st.stop()

# Configure Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
try:
    model = gen_ai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Failed to load Gemini model: {e}")
    st.stop()

# Function to extract text from an uploaded PDF (Multi-page support)
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with fitz.open("pdf", uploaded_file) as doc:  # Open directly without .read()
            for page in doc:
                text += page.get_text("text") + "\n\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

# Function to generate a strong AI prompt
def generate_prompt(user_question, pdf_content):
    return f"""
    Based on the following document:

    {pdf_content[:3000]}  # Limiting to 3000 characters for efficiency

    The user has asked: "{user_question}"
    
    Provide a clear, detailed answer with relevant explanations.
    """

# Streamlit UI
st.title("📄 PDF Q&A Chatbot")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    if not pdf_text.strip():
        st.error("Could not extract any text from the PDF. Please try another file.")
        st.stop()
    
    st.success("PDF Uploaded Successfully! ✅")

    # User selects question type
    query_type = st.radio("Would you like:", ["All topics explained", "Ask a specific question"])

    if query_type == "All topics explained":
        st.info("Generating explanations for all topics in the PDF...")
        
        # Generate AI response
        ai_prompt = generate_prompt("Explain all key topics in detail.", pdf_text)
        try:
            response = model.generate_content(ai_prompt)
            st.markdown("### 📖 Explanation:")
            st.write(response.text if response else "No response from AI.")
        except Exception as e:
            st.error(f"Error generating response: {e}")

    elif query_type == "Ask a specific question":
        user_question = st.text_input("Enter your question:")
        
        if user_question:
            # Generate a prompt using PDF content
            ai_prompt = generate_prompt(user_question, pdf_text)
            try:
                response = model.generate_content(ai_prompt)
                st.markdown("### 💡 Answer:")
                st.write(response.text if response else "No response from AI.")
            except Exception as e:
                st.error(f"Error generating response: {e}")
