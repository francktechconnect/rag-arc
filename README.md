# 🤖 ARC RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for the **Autism Resource Guide (2025)**.  
It uses **ChromaDB** for embeddings, **Streamlit** for the UI, and supports **local (Ollama)** or **hosted LLMs**.

---

## 🚀 Quick Start

```bash
# 1) Clone & enter the repo
git clone <your-repo-url> rag-arc && cd rag-arc

# 2) Seed data (optional): drop PDFs/HTML into ./data
# (You can also add files later from the UI or run the crawler.)

# 3) Configure environment
cp .env.example .env
# Edit .env if needed (LLM_MODE=local recommended for first run)

# 4) Build & start services
docker compose up -d --build

# 5) (one-time) Pull local model for Ollama
docker exec -it ollama ollama pull llama3.1:8b

# 6) Open the UI
# Visit: http://localhost:8501