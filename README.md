# 📡 RAG Telecom Chatbot

A Retrieval-Augmented Generation (RAG) customer care chatbot for telecom support. It answers questions about mobile connectivity, billing, SIM issues, and roaming by retrieving relevant context from three knowledge sources and generating grounded responses via Groq.

## Architecture
User question
│
▼
Merged Retriever (top-k from each store)
├── ChromaDB · faq (FAQ entries from CSV)
├── ChromaDB · tickets (resolved support tickets from SQLite)
└── ChromaDB · guides (PDF guide chunks)
│
▼
ChatPromptTemplate → LLM (Groq) → Answer

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (runs locally via HuggingFace)
**LLM:** `openai/gpt-oss-120b` served by [Groq](https://groq.com)

> Note: this project originally used `qwen/qwen3-32b`, which Groq later deprecated. Groq's model catalog changes over time — if you hit a `model_not_found` error, check currently available models by querying `https://api.groq.com/openai/v1/models` with your API key, and swap in whichever production model is listed at [console.groq.com/docs/models](https://console.groq.com/docs/models).

## Project Structure
rag-telecom-chatbot/
├── app.py # Streamlit web UI
├── main.py # CLI entry point
├── rag_chain.py # Builds the LangChain RAG chain
├── retriever.py # Merges the three Chroma retrievers
├── ingest_faq.py # Loads data/faq.csv into the 'faq' Chroma collection
├── ingest_tickets.py # Loads data/tickets.db into the 'tickets' Chroma collection
├── ingest_pdf.py # Loads data/telecom_guide.pdf into the 'guides' Chroma collection
├── data/
│ ├── faq.csv # FAQ question/answer pairs
│ ├── tickets.db # SQLite database of resolved support tickets
│ ├── telecom_guide.pdf # Telecom user guide (chunked at ingest)
│ ├── seed_tickets.py # Script to seed the tickets database
│ └── generate_pdf.py # Script to generate the telecom guide PDF
├── chroma_store/ # Persisted Chroma vector database (created at ingest)
├── pyproject.toml
├── uv.lock
└── .env.example


## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A free [Groq API key](https://console.groq.com)
- A [HuggingFace token](https://huggingface.co/settings/tokens) *(optional — only avoids a rate-limit warning on the first model download; the app works fine without it)*

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/aleezafatima944-collab/telecom-rag-chatbot.git
cd telecom-rag-chatbot
uv sync
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in your key:

**3. Ingest data into Chroma**

```bash
python ingest_faq.py
python ingest_tickets.py
python ingest_pdf.py
```

Each script embeds the source data and persists it to `chroma_store/`. Re-run a script only when its source data changes.

## Running the App

**Streamlit web UI**

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. The sidebar has one-click sample questions and a button to clear the conversation history.

**CLI**

```bash
python main.py
```

Interactive prompt — type a question and press Enter. Type `quit` to exit.

## Data Sources

| Collection | Source file | Granularity |
|---|---|---|
| `faq` | `data/faq.csv` | 1 document per FAQ row |
| `tickets` | `data/tickets.db` | 1 document per resolved ticket |
| `guides` | `data/telecom_guide.pdf` | Chunks of 600 chars with 100-char overlap |

The retriever fetches the top 3 results from each collection (9 context documents total) for every query.

## Regenerating Seed Data

```bash
python data/seed_tickets.py
python data/generate_pdf.py
```

After regenerating, re-run the corresponding ingest script.

## Possible Improvements

- Retrieval evaluation (precision/recall on a test query set)
- Query routing or hybrid search instead of always searching all 3 collections
- Conversation memory for multi-turn follow-ups
- Re-ranking retrieved chunks before generation
  
