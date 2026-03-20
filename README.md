🔬 Research Assistant RAG

A fully local, chat-based Research Assistant powered by Retrieval Augmented Generation (RAG).
This application allows you to ask questions about your PDF documents and get accurate, source-backed answers — all running locally on your machine.

⚡ No API keys required.
🔒 100% private.
📚 Built for research, learning, and internal knowledge systems.

🚀 Features

📄 PDF Document Processing
Load and process multiple PDF files from a local directory.

🧠 Local LLM (No API Required)
Runs a local model like Gemma-2-2B-IT in GGUF format using CPU — no external services needed.

💾 Efficient Vector Search
Uses FAISS to create and cache embeddings for fast document retrieval.

💬 Interactive Chat UI
Clean and simple interface built with Gradio.

✅ Source Citations
Every answer includes references to the original document and page number.

⚙️ Configurable & Portable
All paths (documents, models, index) are managed via config.py, making it easy to run across different systems.

🧠 How It Works

The application follows a standard RAG pipeline with two main stages:

1️⃣ Ingestion & Indexing (Offline)

Executed only once during the first run.

Load → PDFs are loaded from the /docs folder

Clean → Removes unwanted characters and formatting

Split → Text is divided into smaller overlapping chunks

Embed & Store →

Text chunks are converted into embeddings using all-MiniLM-L6-v2

Stored in a FAISS vector index (/faiss_index)

💡 This step prepares your documents for fast and accurate search.

2️⃣ Retrieval & Generation (Online)

Runs every time you ask a question.

Retrieve → Finds the most relevant document chunks

Augment → Combines retrieved context with your query

Generate →
The local LLM generates a response based only on the provided context

🎯 Ensures accurate, context-aware answers with minimal hallucination.

⚙️ Setup & Usage
✅ Prerequisites

Python 3.10 – 3.12

Git

OS: Windows / macOS / Linux (Ubuntu recommended)

1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
2️⃣ Create Required Folders
mkdir docs
mkdir models
mkdir faiss_index
3️⃣ Add Your Files

Place your .pdf files inside the docs folder

Download the Gemma-2-2B-IT GGUF model (recommended: Q4_K_M)

Add the .gguf file to the models folder

4️⃣ Install Dependencies
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
5️⃣ Run the Application
python app.py

First run → creates FAISS index (may take a few minutes)

Then launches a local web UI (e.g. http://127.0.0.1:7860
)

🧱 Tech Stack

Framework → LangChain

LLM → Gemma-2 (via Llama.cpp)

Embeddings → Sentence-Transformers

Vector Store → FAISS

Frontend UI → Gradio

🎯 Use Cases

📚 Research paper assistant

🏢 Internal company knowledge bot

📄 Document Q&A system

🎓 Study assistant

🧠 Key Highlights

🔒 Fully offline & private

💸 No API costs

⚡ Fast retrieval after indexing

📌 Accurate answers with citations

📌 Summary

This project demonstrates how to build a production-style local RAG system that combines:

Document understanding

Semantic search

Local AI generation

👉 All in a simple, extensible architecture.
