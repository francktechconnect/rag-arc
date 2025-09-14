# Placeholder for app/crew_flow.py
import os
from crewai import Agent, Task, Crew
from app.crawler import SimpleCrawler
from app.ingest import Ingestor
from app.rag import RAG
from app.utils import list_files as ingressible_files

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def load_prompt(name: str):
    path = os.path.join(PROMPTS_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def meta_optimize(task_desc: str):
    # Simplified meta-optimizer placeholder
    return {
        "prompt": f"Do: {task_desc}. Provide JSON result with 'result' and 'metrics'.",
        "checks": ["Inputs present", "Outputs present", "Done criteria clear"],
        "critique": "Kept minimal to avoid overfitting.",
    }


class Flow:
    def __init__(self, data_dir: str, chroma_dir: str):
        self.data_dir = data_dir
        self.chroma_dir = chroma_dir

    def run_download(self, base_url: str):
        crawler = SimpleCrawler(base_url, self.data_dir)
        saved = crawler.crawl()
        return {"files": saved, "count": len(saved)}

    def run_ingest(self):
        ing = Ingestor(self.data_dir, self.chroma_dir)
        files = list(ingressible_files(self.data_dir))
        return ing.upsert_files(files)

    def run_qa(self, question: str):
        rag = RAG(self.data_dir, self.chroma_dir)
        return rag.answer(question)
