# 🚀 Pitch Deck Analyst

Analyze your startup pitch decks in seconds using AI!  
This tool extracts a business summary and team analysis from uploaded PDF pitch decks.

---

## 📝 Overview & Features

- **Upload** your PDF pitch deck.
- **Automatic AI analysis** of:
  - **Business Summary**: Product, customer, and problem.
  - **Team Analysis**: Founders, roles, and experience.
- **Download** the analysis as a text file.
- Fast, private, and requires only your Gemini API key.

---

## 🖼️ How it looks like!

<!-- Add your screenshots here -->
![Screenshot 1]()
![Screenshot 2]()

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: Flask
- **AI/LLM**: Google Gemini API (via `google-generativeai`)
- **Vector Store**: ChromaDB
- **PDF Processing**: PyPDF, LangChain

---

## 📦 API Used

- [Google Gemini Generative AI API](https://ai.google.dev/)
  - For generating summaries and extracting key information from pitch decks.

---

## ⚡ Installation & Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/<-your username->/irst_pass_analysis_agent.git
   cd first_pass_analysis_agent
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Add your Google Gemini API key to a `.env` file:
   echo "GEMINI_API_KEY=your_key_here" > .env
   python app.py
   ```

3. **Frontend Setup:**
   ```bash
   cd ..
   pip install streamlit requests
   streamlit run app.py
   ```

4. **Usage:**
   - Open the Streamlit app in your browser.
   - Upload a PDF pitch deck and click "Analyze".
   - View and download the automatic analysis.

---

## 🧑‍💻 Curated with ❤️ by Avan

---

> _Note: Works best with text-based PDFs. Scanned documents may not yield accurate results._
