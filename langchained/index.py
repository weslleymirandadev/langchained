"""Turn a folder of text files into a JSON list of chunks."""

import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

INDEX_DIR = ".langchained"
INDEX_FILE = "index.json"


def find_files(path):
    if os.path.isfile(path):
        return [path]
    files = []
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if full.endswith(".md") or full.endswith(".txt"):
            files.append(full)
    return files


def chunk_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n\n", "\n", " "],
    )
    chunks = []
    for piece in splitter.split_text(text):
        chunks.append({"source": os.path.basename(path), "text": piece.strip()})
    return chunks


def build_index(path):
    chunks = []
    for file in find_files(path):
        chunks.extend(chunk_file(file))

    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(os.path.join(INDEX_DIR, INDEX_FILE), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    return chunks


def load_index():
    path = os.path.join(INDEX_DIR, INDEX_FILE)
    if not os.path.exists(path):
        raise SystemExit("No index found. Run: python -m langchained ingest samples")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
