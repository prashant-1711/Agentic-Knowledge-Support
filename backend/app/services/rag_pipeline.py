from dotenv import load_dotenv
import os
from google import genai

from app.retrieval.search import search_chunks

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def build_context(results, max_chars: int = 6000) -> str:
    """
    Build a compact context block from retrieved chunks.
    Keeps the most relevant chunks and trims very long text.
    """
    parts = []
    total_chars = 0

    for i, item in enumerate(results, start=1):
        chunk_text = item["content"].strip()
        source = f'Source {i}: file="{item["filename"]}", chunk={item["chunk_index"]}, distance={item["distance"]:.4f}'

        block = f"{source}\n{chunk_text}\n"
        if total_chars + len(block) > max_chars:
            break

        parts.append(block)
        total_chars += len(block)

    return "\n---\n".join(parts)


def generate_answer(query: str, top_k: int = 5) -> dict:
    """
    1. Retrieve relevant chunks from pgvector
    2. Build a context block
    3. Ask Gemini to answer using only that context
    4. Return answer + sources
    """
    results = search_chunks(query, top_k=top_k)

    if not results:
        return {
            "query": query,
            "answer": "I could not find relevant information in the documents.",
            "sources": [],
        }

    context = build_context(results)

    prompt = f"""
You are an internal knowledge support assistant.

Answer the user's question using ONLY the provided context.
If the answer is not in the context, say:
"I could not find this information in the uploaded documents."

Rules:
- Be concise and accurate.
- Do not invent facts.
- If possible, mention the section or file name from the context.
- Do not mention distances or vector search.

User question:
{query}

Context:
{context}
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "query": query,
        "answer": response.text,
        "sources": [
            {
                "filename": item["filename"],
                "chunk_index": item["chunk_index"],
                "distance": item["distance"],
            }
            for item in results
        ],
    }