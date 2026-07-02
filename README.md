# Build a Conversational SHL Assessment Recommender

A conversational AI-powered recommendation system that recommends suitable SHL assessments based on hiring requirements. The application combines Retrieval-Augmented Generation (RAG) with Google Gemini to provide context-aware recommendations, clarification questions, assessment comparison, and recommendation refinement through a conversational interface.

---

## Overview

The system retrieves relevant SHL assessments from the provided assessment catalogue and generates conversational responses using Google Gemini 2.5 Flash. Instead of relying solely on the language model, the application first retrieves relevant assessment information and then uses the retrieved context to generate accurate responses.

The application supports:

- Multi-turn conversations
- Clarification for ambiguous hiring requirements
- Recommendation refinement
- Assessment comparison
- Public REST API using FastAPI

---

## Features

- Conversational SHL assessment recommendation
- Multi-turn conversation support
- Clarification questions before recommendation
- Assessment comparison
- Recommendation refinement using conversation history
- Lightweight TF-IDF retrieval pipeline
- FastAPI REST API
- Public deployment on Render

---

## Tech Stack

- Python
- FastAPI
- Google Gemini 2.5 Flash
- Scikit-learn (TF-IDF + Cosine Similarity)
- NumPy
- Render
- Git & GitHub

---

## Project Structure

```text
.
├── main.py                  # FastAPI application
├── llm.py                   # LLM prompts and response generation
├── catalog.json             # SHL assessment catalogue
├── requirements.txt
├── test_traces.py           # Evaluation script
├── README.md
└── .env                     # Local environment variables (ignored by Git)
```

---

## Solution Workflow

1. Receive the complete conversation history.
2. Decide whether enough information is available or a clarification question is required.
3. Rewrite the conversation into a retrieval-friendly search query.
4. Retrieve relevant SHL assessments using TF-IDF and cosine similarity.
5. Generate a conversational response using Google Gemini based only on the retrieved assessment information.

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns the application status.

---

### Chat

```http
POST /chat
```

Example request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend assessments for a Java Backend Developer with 2 years of experience."
    }
  ]
}
```

---

## Running Locally

### Clone the repository

```bash
git clone https://github.com/smritii-22/shl-recommender.git
cd shl-recommender
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it:

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Start the application

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Deployment

The application is deployed on Render.

**Deployment URL**

https://shl-recommender-qt12.onrender.com

---

## Evaluation

The implementation was evaluated using:

- Provided conversation traces
- Ambiguous hiring scenarios
- Multi-turn conversations
- Recommendation refinement
- Assessment comparison
- Legal/compliance requests
- Public deployment verification

---

## Design Decisions

- FastAPI for REST API implementation
- TF-IDF retrieval for lightweight deployment
- Conversation-aware recommendation workflow
- Separate prompts for planning, query rewriting, clarification, and response generation
- Modular code organization for maintainability

---

## Future Improvements

- Hybrid semantic retrieval using transformer embeddings
- Persistent conversation memory
- Confidence scoring for recommendations
- Result caching
- Support for additional assessment catalogues

---

## Acknowledgements

This project was developed as part of the **Build a Conversational SHL Assessment Recommender – Take-home Assignment for AI Intern Role**.

Official documentation referred during development:

- FastAPI
- Google Gemini
- Render
- Scikit-learn

---

## Author

**Smriti**
