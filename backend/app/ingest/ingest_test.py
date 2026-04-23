from app.ingest.embedder import get_embedding

vec = get_embedding("Employee leave policy")
print(len(vec))
print(vec[:5])