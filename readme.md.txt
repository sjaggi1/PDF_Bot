📄 PDF Q&A Chatbot

A Streamlit-based chatbot that answers questions from PDFs using Google's Gemini AI.

🚀 Features
- Upload a PDF and extract text.
- Ask questions about the PDF or get a summary.
- Uses Google Gemini AI for intelligent responses.

🛠️ Installation
1. Clone the repository:
   git clone https://github.com/sjaggi1/PDF_Bot.git

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

4. Install dependencies:
   pip install -r requirements.txt

-> Usage

1. Set your Google API Key in a .env file:
	GOOGLE_API_KEY=your_api_key_here

2. Run the chatbot:
	streamlit run app.py

3. Upload a PDF and ask questions!