# Placeholder for app/utils.py
import os, re
from pathlib import Path


def safe_filename(url_or_name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", url_or_name)
    return name[:200]


def list_files(data_dir: str):
    exts = {".txt", ".md", ".pdf", ".html"}
    for p in Path(data_dir).rglob("*"):
        if p.suffix.lower() in exts and p.is_file():
            yield str(p)