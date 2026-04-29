from dotenv import load_dotenv
import os
from math import sqrt
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def _normalize(vector):
    norm = sqrt(sum(x * x for x in vector))
    if norm == 0:
        return vector
    return [x / norm for x in vector]


def get_embedding(
    text: str,
    task_type: str = "retrieval_document",
    output_dimensionality: int = 768,
):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": task_type,
            "output_dimensionality": output_dimensionality,
        },
    )

    return _normalize(response.embeddings[0].values)