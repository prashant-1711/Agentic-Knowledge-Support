import re
from typing import List, Dict


def clean_text(text: str) -> str:
    """
    Basic cleanup:
    - normalize line endings
    - remove extra spaces
    - keep paragraph breaks
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Remove repeated spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce 3+ newlines to 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    return text.strip()


def split_long_text(text: str, max_chars: int, overlap_chars: int) -> List[str]:
    """
    Split a long text into overlapping chunks.
    This is a simple character-based chunker, good for starting out.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + max_chars
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap_chars
        if start < 0:
            start = 0

    return chunks


def chunk_text(text: str, max_chars: int = 1200, overlap_chars: int = 200) -> List[str]:
    """
    Chunk text using paragraph-aware splitting first.
    If a paragraph is too large, split it further.
    """
    text = clean_text(text)

    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    final_chunks = []
    current_chunk = ""

    for para in paragraphs:
        # If one paragraph is too large, split it first
        if len(para) > max_chars:
            if current_chunk:
                final_chunks.append(current_chunk.strip())
                current_chunk = ""

            final_chunks.extend(split_long_text(para, max_chars, overlap_chars))
            continue

        # Try adding paragraph to current chunk
        if not current_chunk:
            current_chunk = para
        elif len(current_chunk) + len(para) + 2 <= max_chars:
            current_chunk += "\n\n" + para
        else:
            final_chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk.strip():
        final_chunks.append(current_chunk.strip())

    return final_chunks


def make_chunk_records(text: str, filename: str, max_chars: int = 1200, overlap_chars: int = 200) -> List[Dict]:
    """
    Convert raw text into DB-ready chunk records.
    """
    chunks = chunk_text(text, max_chars=max_chars, overlap_chars=overlap_chars)

    records = []
    for i, chunk in enumerate(chunks):
        records.append({
            "filename": filename,
            "chunk_index": i,
            "content": chunk,
        })

    return records