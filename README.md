# Placeholder for README.md
# 1) Clone & cd
# git clone <your-repo-url> rag-test-arc && cd rag-test-arc


# 2) Seed data (optional): drop PDFs/HTML into ./data
# (You can also add files later from the UI or run the crawler.)


# 3) Configure
cp .env.example .env
# edit .env if needed (LLM_MODE=local recommended first run)


# 4) Start
docker compose up -d --build


# 5) (one-time) pull local model for Ollama
docker exec -it ollama ollama pull llama3.1:8b


# 6) Open UI
# http://localhost:8501


# 7) Click "Ingest / Refresh Index" then ask a question