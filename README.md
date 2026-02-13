# Construction Marketplace RAG System

A Retrieval-Augmented Generation (RAG) system for construction marketplace queries using semantic search and LLM-powered responses.

## Features

- **Semantic Search** - FAISS vector index with sentence-transformers embeddings
- **Grounded Answers** - LLM responses strictly based on retrieved context
- **Source Attribution** - Shows retrieved chunks with sources and similarity scores
- **Multiple LLM Options** - Groq (fast), OpenRouter, Ollama (offline)
- **Streamlit UI** - Clean Python-based chat interface
- **Quality Evaluation** - Automated testing script

## Architecture

```
User Question
     ↓
[Embedding Model] sentence-transformers/all-MiniLM-L6-v2
     ↓
[Vector Search] FAISS top-5 similarity search
     ↓
[Retrieved Chunks] With sources + scores
     ↓
[LLM] Groq/OpenRouter/Ollama with grounding prompt
     ↓
Grounded Answer
```

## Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/rag-construction.git
cd rag-construction

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from https://console.groq.com

# 5. Run the app
streamlit run app.py
```

**Open**: http://localhost:8501

### First Time Setup

1. Click **"Build Index"** in the sidebar
2. Wait for index to build (~30 seconds)
3. Start asking questions!

## Configuration

Create a `.env` file with your API keys:

```bash
# Groq (Recommended - Fast & Free)
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Embedding Model
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# Optional: Offline Mode
USE_OLLAMA=false
OLLAMA_MODEL=llama3.2
```

**Get Groq API Key**: [console.groq.com](https://console.groq.com/) (Free tier available)

## Usage

### Add Your Documents

Place your construction documents (`.txt` or `.md` format) in the `data/` folder:

```
data/
  ├── doc1.md
  ├── doc2.md
  └── doc3.md
```

### Running the App

```bash
streamlit run app.py
```

### Using the Interface

1. **Build Index** - Click "Build Index" in sidebar (first time only)
2. **Select Mode** - Choose "Online (Groq)" or "Offline (Ollama)"
3. **Ask Questions** - Type or use sample questions from sidebar
4. **View Context** - Expand sections to see retrieved document chunks

## Deployment to Streamlit Cloud (Free!)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - RAG system"

# Create repository on GitHub, then:
git remote add origin https://github.com/yourusername/rag-construction.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `yourusername/rag-construction`
4. Set main file: `app.py`
5. Click **"Advanced settings"** → **"Secrets"**
6. Add your API key:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   LLM_PROVIDER = "groq"
   ```
7. Click **"Deploy"**
8. Wait 2-3 minutes for deployment
9. Get your public URL: `https://your-app.streamlit.app`

### Step 3: Share Your Demo

Your app is now live! Share the URL for your assignment submission.

**Note**: First-time visitors should click "Build Index" before asking questions.

## Project Structure

```
rag_implement/
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── rag/                   # Core RAG logic
│   ├── config.py         # Configuration
│   ├── embeddings.py     # Sentence transformers
│   ├── ingest.py         # Document processing
│   ├── llm.py           # LLM integration
│   ├── retriever.py     # Vector search
│   └── vector_store.py  # FAISS index
├── data/                 # Document storage
└── .streamlit/          # Streamlit configuration
```

## How It Works

### Document Processing

1. Load `.txt` or `.md` files from `data/` folder
2. Chunk text (800 chars with 200-char overlap)
3. Generate embeddings using sentence-transformers
4. Build FAISS index and save metadata

### Query Processing

1. User asks a question
2. Convert question to embedding
3. Retrieve top-5 similar chunks from FAISS
4. Build prompt with retrieved context
5. Send to LLM (Groq/Ollama)
6. Display answer with sources

## Quality Evaluation

Run automated testing:

```bash
python evaluate_quality.py
```

Results saved to `evaluation_results.json` and `EVALUATION_RESULTS.md`

## Sample Questions

Try these questions based on the included construction documents:

1. "What is Indecimal's delay management policy?"
2. "How many quality checks does Indecimal perform?"
3. "What are the customer journey stages?"
4. "How does the escrow payment system work?"
5. "What makes Indecimal different from competitors?"

## Technologies Used

- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **LLM**: Groq API (llama-3.1-8b-instant)
- **Framework**: Streamlit for UI, FastAPI as alternative
- **Chunking**: Character-based with overlap

## Troubleshooting

**"Index not found" error:**
- Click "Build Index" button in sidebar
- Wait for confirmation message

**Slow first load:**
- Streamlit downloads embedding model (~80MB) on first run
- Subsequent loads are fast

**API errors:**
- Verify GROQ_API_KEY in `.env` or Streamlit Cloud secrets
- Check API key is valid at https://console.groq.com/

## License

MIT License - feel free to use for educational purposes
