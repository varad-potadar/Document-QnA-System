📄 Research Paper Question Answering System

A lightweight research assistant that allows users to upload academic PDF papers and ask questions grounded strictly in the paper’s content.
The system uses local document processing, semantic retrieval, and Groq-powered LLM reasoning to provide accurate, non-hallucinated answers.
This project focuses on clarity, correctness, and simplicity, avoiding unnecessary infrastructure and overengineering.


✨ Key Features

Upload and process academic research papers (PDF)
Robust text extraction from single- and multi-column papers
Intelligent text chunking with overlap
Semantic retrieval using FAISS
Accurate, document-grounded answers
Clean, minimal Streamlit user interface
Fast inference using Groq LLM API
Secure API key handling via environment variables


🧠 System Architecture
Streamlit UI
     ↓
PDF Text Extraction (PyMuPDF)
     ↓
Text Chunking
     ↓
Embeddings (Sentence Transformers)
     ↓
FAISS Vector Search
     ↓
Groq LLM (Answer Generation)
means grounded answers


🛠️ Tech Stack
Core
Python
Streamlit

NLP & Retrieval
PyMuPDF (PDF text extraction)
Sentence-Transformers (MiniLM)
FAISS (vector similarity search)

LLM
Groq API


📂 Project Structure
.
├── app.py                  # Streamlit application (entry point)
├── services/
│   ├── pdf_extractor.py    # PDF text extraction
│   ├── chunker.py          # Text chunking logic
│   ├── embedder.py         # Embedding generation
│   ├── vector_store.py     # FAISS vector store
│   └── qa_engine.py        # Groq-powered Q&A logic
├── requirements.txt
├── README.md
└── .gitignore


⚙️ Setup Instructions (Local)
1️⃣ Clone the repository
git clone <your-repo-url>
cd research-paper-qna

2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variable
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here

5️⃣ Run the app
streamlit run app.py

The application will open at:
http://localhost:8501

🌐 Deployment (Streamlit Cloud)

Push the project to GitHub (without .env)
Go to https://streamlit.io/cloud
Create a new app from your repository

Set Main file path to:
app.py

Add the following Secret:
GROQ_API_KEY = "your_groq_api_key_here"

Deploy
Streamlit Cloud will handle installation and execution automatically.


🔐 Security & API Key Handling

API keys are never hardcoded
.env is ignored via .gitignore
Streamlit Cloud secrets are used for production
Keys are accessed via os.getenv("GROQ_API_KEY")
This ensures the API key is never exposed in the repository or UI.


🔍 Design Decisions & Rationale

Groq-only LLM usage
Reduces complexity and avoids multiple external dependencies.

Local embeddings and retrieval
Improves reliability and debuggability.

No section-based PDF heuristics
Avoids brittle logic that often fails on academic PDFs.

Streamlit for UI
Prioritizes usability and clarity over frontend complexity.

The goal is a robust research prototype, not a SaaS product.


⚠️ Limitations

Single document per session
No persistent storage between sessions
Optimized for text-based PDFs (not scanned images)
These limitations are intentional to keep the system simple and stable.


🚀 Possible Future Improvements

Citation highlighting in answers
Multi-document support
Answer confidence scoring
Export answers with references
Improved PDF layout handling


📌 Project Purpose

This project demonstrates:
End-to-end document understanding
Retrieval-Augmented Generation (RAG)
Practical LLM integration
Debugging and system design skills
Secure deployment practices


📜 License

This project is intended for educational and demonstration purposes.
