from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": "retrieval_document",
            "output_dimensionality": 768
        }
    )

    return response.embeddings[0].values