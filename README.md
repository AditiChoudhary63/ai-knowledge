# AI Knowledge Assistant

A simple AI-powered knowledge assistant built with **FastAPI, RAG, LangGraph, and LLMs**.
It allows you to store text as `.txt` files and ask questions that are answered using document-based retrieval.

---

## What This Project Does

1. Accepts raw text via API
2. Saves the text as `.txt` files
3. Chunks and embeds documents
4. Stores embeddings in a vector database
5. Uses RAG to answer questions accurately

---

## Tech Stack

* FastAPI
* LangGraph
* OpenAI LLM & Embeddings
* Chroma Vector DB
* File-based document storage (`.txt`)

---

## Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Set environment variable

```env
OPENAI_API_KEY=your_api_key_here
```

3. Run the app

```bash
uvicorn main:app --reload
```

---

## Add a Document

```
POST /documents
```

```json
{
  "text": "Authentication uses JWT tokens validated using a shared secret."
}
```

This saves the text as a `.txt` file and indexes it for RAG.

---

## Ask a Question

```
POST /ask
```

```json
{
  "question": "How does authentication work?"
}
```

Response:

```json
{
  "answer": "Authentication is handled using JWT tokens..."
}
```

---

## How It Works (Simple)

```
Text → .txt file → Chunk → Embed → Vector DB → Retrieve → LLM Answer
```

---

##  Use Case

* Internal documentation Q&A
* Engineering knowledge base
* AI-powered notes search

---
