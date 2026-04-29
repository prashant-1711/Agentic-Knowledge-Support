import re
from typing import List, Dict


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def split_by_headings(text: str) -> List[str]:
    """
    Split text into sections using headings like:
    1.
    1.1
    10.2
    """
    pattern = r"\n(?=\d+\.\d+|\d+\.)"
    sections = re.split(pattern, text)

    return [s.strip() for s in sections if s.strip()]


def chunk_section(section: str, max_chars=800, overlap=100) -> List[str]:
    """
    Further split large sections
    """
    chunks = []
    start = 0

    while start < len(section):
        end = start + max_chars
        chunk = section[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(section):
            break

        start = end - overlap

    return chunks


def make_chunk_records(text: str, filename: str) -> List[Dict]:
    text = clean_text(text)

    sections = split_by_headings(text)

    records = []
    chunk_id = 0

    for section in sections:
        chunks = chunk_section(section)

        for chunk in chunks:
            records.append({
                "filename": filename,
                "chunk_index": chunk_id,
                "content": chunk
            })
            chunk_id += 1

    return records