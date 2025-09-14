# Placeholder for app/rag.py
import os
from typing import Dict
from app.ingest import Ingestor
from app.providers import LLMProvider

SYS_PROMPT = (
    "You are a careful assistant that answers ONLY from provided context. "
    "Always cite filenames and chunk numbers like [source:chunk]. "
    "If unsure, say in a professional manner you do not have that information and refer"
    "to the website of ARC."
)


class RAG:
    def __init__(self, data_dir: str, chroma_dir: str):
        self.ing = Ingestor(data_dir, chroma_dir)
        self.llm = LLMProvider()

    def retrieve(self, q: str, k: int = 4):
        return self.ing.search(q, k)

    def answer(self, question: str, k: int = 4) -> Dict:
        res = self.retrieve(question, k)
        ctx_blocks = []
        cites = []

        for i in range(len(res.get("documents", [[]])[0])):
            doc = res["documents"][0][i]
            meta = res["metadatas"][0][i]
            src = meta.get("source", "unknown")
            filename = os.path.splitext(os.path.basename(src))[0]  # strip folder + .pdf
            #filename = filename.replace("+", "-")                  # replace + with -
            ch = meta.get("chunk", "?")
            ctx_blocks.append(f"[source {i}] ({src} :: section {ch})\n{doc}")
            cites.append(f"{filename}:{ch}")
            #cites.append(f"{src}:{ch}")

        context = "\n\n".join(ctx_blocks) if ctx_blocks else "(no results)"

        messages = [
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"},
        ]
        completion = self.llm.chat(messages)
        return {"answer": completion, "citations": cites}
