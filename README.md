# PDF AI Assistant

## Overview
The **PDF AI Assistant** is a Streamlit-powered application that allows users to interact with PDFs by entering a PDF URL and asking questions about its content. The application leverages **Groq LLM, Gemini Embeddings, and PostgreSQL (pgvector)** for efficient retrieval-augmented generation (RAG) capabilities.

## Features
- 📄 **Upload PDFs via URL**: Enter a link to a PDF file and interact with it.
- 🤖 **AI-Powered Chat**: Ask questions related to the uploaded PDF, and get AI-generated answers.
- 🔍 **Knowledge Base**: The app stores and retrieves information from PDFs using **pgvector**.
- 🗃️ **Persistent Chat History**: Stores user sessions in **PostgreSQL** for context retention.

## Prerequisites
Ensure you have the following installed on your system:
- [Docker](https://www.docker.com/get-started)
- Python 3.8+
- PostgreSQL (running in Docker)

## Setup

### 1. Clone the Repository
```sh
 git clone https://github.com/Zaheerkhn/PDF-Assistant
 cd pdf-ai-assistant
```

### 2. Set Up PostgreSQL with pgvector
To use this application, you need to set up PostgreSQL with the **pgvector** extension. Run the following command in **Git Bash** (ensure Docker is installed and running):

```sh
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```
This will start a **PostgreSQL** instance with **pgvector** enabled on port `5532`.

### 3. Install Dependencies
Create a virtual environment and install the required dependencies:
```sh
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add:
```env
GROQ_API_KEY=<your_groq_api_key>
GOOGLE_API_KEY=<your_google_api_key>
```

### 5. Run the Application
Start the Streamlit app:
```sh
streamlit run app.py
```

## How It Works
1. Enter a **PDF URL** in the input field.
2. The application processes the PDF, extracts text, and stores embeddings in **pgvector**.
3. Ask questions related to the document, and the AI will retrieve the most relevant information.
4. The chat history is saved for context retention in **PostgreSQL**.

## Tech Stack
- **Streamlit** – Frontend UI
- **Groq LLM** – Language model for answering queries
- **Gemini Embeddings** – Text embedding for similarity search
- **PostgreSQL + pgvector** – Vector database for efficient retrieval
- **Docker** – Containerized PostgreSQL setup

## Contribution
Feel free to contribute to this project by submitting issues or pull requests!

## License
This project is licensed under the **Apache License 2.0**.


