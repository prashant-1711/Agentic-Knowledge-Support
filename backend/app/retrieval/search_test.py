from app.retrieval.search import search_chunks

results = search_chunks("How many sick leaves are allowed?", top_k=3)

for r in results:
    print("=" * 80)
    print("File:", r["filename"])
    print("Chunk:", r["chunk_index"])
    print("Distance:", r["distance"])
    print(r["content"][:800])