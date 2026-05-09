# Agentic Knowledge Support (IKS)

An internal knowledge support agent that answers employee questions from company documents using retrieval-augmented generation (RAG), vector search, and a structured chat workflow.

## Overview

This project is designed to help users ask natural-language questions and get grounded answers from internal documents such as employee handbooks, onboarding guides, HR policies, IT policies, and other internal reference material.

The system ingests documents, splits them into chunks, generates embeddings, stores them in PostgreSQL with pgvector, retrieves the most relevant chunks for a question, and then uses Gemini to generate a grounded response.

The project was built as a full-stack AI application with a FastAPI backend and a lightweight Gradio frontend.

## Key Features

* Upload and process internal PDF documents
* Chunk documents into smaller semantic pieces
* Store embeddings in PostgreSQL with pgvector
* Retrieve relevant passages using similarity search
* Generate grounded answers with Gemini
* Return source-aware responses
* Support batch processing to handle API limits reliably
* Use time buffering and retry-safe processing for stable ingestion
* Separate backend and frontend for maintainability

## Tech Stack

### Backend

* Python 3.10
* FastAPI
* Gemini API
* PostgreSQL
* pgvector
* Pydantic
* pdfplumber / PDF text extraction utilities
* python-dotenv

### Frontend

* Gradio

### Infrastructure / DevOps

* Docker
* Git / GitHub

## How It Works

### 1. Document Ingestion

Documents are loaded from the sample documents folder or uploaded by the user. The backend extracts text from PDFs and prepares it for chunking.

### 2. Chunking

Large documents are split into smaller chunks so that each chunk can be embedded and searched efficiently. This improves retrieval quality and avoids sending oversized inputs to the model.

### 3. Embedding and Storage

Each chunk is converted into a vector embedding and stored in PostgreSQL using pgvector. The database acts as the knowledge store for retrieval.

### 4. Retrieval

When a user asks a question, the system converts the query into a vector and searches for the most relevant chunks using similarity search.

### 5. Answer Generation

The retrieved chunks are sent to Gemini along with the user question. Gemini generates a response grounded in the retrieved context.

### 6. Structured Output

The response is formatted in a predictable structure so the frontend can display it cleanly and the backend can handle it safely.

## Project Structure

```text
agentic-knowledge-support/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── db/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── app.py
├── data/
│   └── sample_docs/
├── docker/
└── README.md
```

## Setup

### Prerequisites

* Python 3.10
* PostgreSQL installed locally
* pgvector extension enabled
* Gemini API key
* Git
* Docker (optional for local infra and experimentation)

### Install Dependencies

From the backend folder:

```bash
pip install -r requirements.txt
```

If you are installing manually, the main dependencies include:

* fastapi
* uvicorn
* google-generativeai or the Gemini SDK used in the project
* psycopg2-binary
* pgvector
* python-dotenv
* pydantic
* pdfplumber
* gradio

### Environment Variables

Create a `.env` file inside `backend/` and add the required keys such as:

```env
GEMINI_API_KEY=your_api_key_here
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit real secrets to GitHub.

### Database Setup

Make sure PostgreSQL is running and pgvector is enabled in the target database.

Example:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Running the Project

### Backend

Start the FastAPI backend from the backend directory:

```bash
uvicorn app.main:app --reload
```

### Frontend

Start the Gradio app from the frontend directory:

```bash
python app.py
```

## Sample Documents

The project was tested with public employee handbook and policy-style PDFs to simulate an internal company knowledge base. These documents are used only as sample sources for testing retrieval and grounded QA.

## Hurdles Solved During Development

Several practical issues came up during development and were solved as part of the project:

* **PDF ingestion pipeline was built to handle large documents reliably**

  * PDFs were extracted into plain text before processing.
  * Long documents were split into manageable chunks for downstream embedding and retrieval.

* **Chunk size was increased and tuned for better context retention**

  * Chunking was adjusted so each chunk carried enough surrounding context to preserve meaning.
  * This improved answer quality while still keeping retrieval efficient.

* **Overlapping chunks were added to reduce information loss at boundaries**

  * Small overlaps between chunks helped preserve continuity across split sections.
  * This made it less likely that an important line or policy detail would be missed during retrieval.

* **Docker-based pgvector setup was resolved successfully**

  * pgvector was installed through a Dockerized Ubuntu environment.
  * The container was then connected to PostgreSQL so vector search could work correctly.

## Security Notes

* API keys are stored in `.env` and must never be committed.
* Internal or confidential documents should not be uploaded to the public repository.
* Sample documents used in the repo should remain public, synthetic, or non-sensitive.
* The system should be used with access controls if adapted to a real internal environment.

## What This Project Demonstrates

This project demonstrates practical AI engineering skills including:

* document ingestion
* chunking and preprocessing
* vector database usage
* retrieval-augmented generation
* structured output handling
* backend API development
* frontend integration
* prompt and workflow design
* error handling and reliability improvements
* deployment-aware engineering with Docker

## Future Improvements

Potential next steps for the project include:

* better document upload UI
* richer citation display
* multi-user memory
* confidence scoring and escalation flow
* role-based access control
* improved evaluation metrics
* analytics dashboard for queries and retrieval quality

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Built as a practical internal knowledge support system for employee queries, document search, and grounded AI assistance.
