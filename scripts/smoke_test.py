# Placeholder for scripts/smoke_test.py
import os
import sys 

# ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag import RAG

DATA_DIR = os.getenv("DATA_DIR", "./data")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./storage")

if __name__ == "__main__":
    rag = RAG(DATA_DIR, CHROMA_DIR)
    q = "List two programs mentioned for parents of autistic children"
    print(rag.answer(q))
