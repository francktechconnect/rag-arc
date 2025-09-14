# Placeholder for app/ingest.py
import os
from pathlib import Path
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils import list_files


class Ingestor:
    def __init__(
        self,
        data_dir: str,
        chroma_dir: str,
        collection_name: str = "arc_docs",
        embed_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.data_dir = data_dir
        self.client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer(embed_model)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=120
        )

    def read_text(self, path: str) -> str:
        p = Path(path)
        if p.suffix.lower() == ".pdf":
            # Use pdftotext via poppler-utils (installed in Docker)
            import subprocess
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                subprocess.run(["pdftotext", str(p), tmp.name], check=True)
                txt = Path(tmp.name).read_text(encoding="utf-8", errors="ignore")
            return txt
        else:
            return p.read_text(encoding="utf-8", errors="ignore")

    def upsert_files(self, files: List[str]):
        ids, docs, metas = [], [], []
        for f in files:
            raw = self.read_text(f)
            chunks = self.splitter.split_text(raw)
            for i, ch in enumerate(chunks):
                ids.append(f"{f}::chunk::{i}")
                docs.append(ch)
                metas.append({"source": f, "chunk": i})
        if not docs:
            return {"docs_indexed": 0, "chunks": 0}
        embs = self.embedder.encode(docs, show_progress_bar=True).tolist()
        self.collection.upsert(
            ids=ids, embeddings=embs, documents=docs, metadatas=metas
        )
        return {
            "docs_indexed": len(set([m["source"] for m in metas])),
            "chunks": len(docs),
        }

    def search(self, query: str, k: int = 4):
        q_emb = self.embedder.encode([query]).tolist()[0]
        return self.collection.query(query_embeddings=[q_emb], n_results=k)


if __name__ == "__main__":
    data_dir = os.environ.get("DATA_DIR", "./data")
    chroma_dir = os.environ.get("CHROMA_DIR", "./storage")
    ing = Ingestor(data_dir, chroma_dir)
    files = list(list_files(data_dir))
    print(ing.upsert_files(files))
