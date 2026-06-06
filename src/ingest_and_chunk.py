from pathlib import Path
from docx import Document
import re
import json
import random

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/chunks")

CHUNK_SIZE = 350
OVERLAP = 75

def load_docx(file_path):
    doc = Document(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("Read more", "")
    text = text.replace("Share", "")
    text = text.strip()
    return text


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    all_chunks = []

    docx_files = sorted(RAW_DIR.glob("*.docx"))

    print(f"Found {len(docx_files)} documents.")

    for file_path in docx_files:
        raw_text = load_docx(file_path)
        cleaned_text = clean_text(raw_text)

        processed_path = PROCESSED_DIR / f"{file_path.stem}.txt"
        processed_path.write_text(cleaned_text, encoding="utf-8")

        chunks = chunk_text(cleaned_text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{file_path.stem}_chunk_{i}",
                "source": file_path.name,
                "chunk_number": i,
                "text": chunk
            })

    output_path = CHUNKS_DIR / "chunks.json"
    output_path.write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")

    print(f"Created {len(all_chunks)} total chunks.")
    print(f"Saved chunks to {output_path}")

    print("\n--- 5 Random Chunks for Inspection ---\n")
    sample_chunks = random.sample(all_chunks, min(5, len(all_chunks)))

    for chunk in sample_chunks:
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['id']}")
        print(chunk["text"])
        print("-" * 80)


if __name__ == "__main__":
    main()