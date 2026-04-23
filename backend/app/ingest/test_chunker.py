from pdf_loader import load_pdfs_from_folder
from chunker import make_chunk_records

docs = load_pdfs_from_folder(r"D:\Agentic Knowledge Support\data\sample_doc")

for doc in docs:
    print("=" * 80)
    print("FILE:", doc["filename"])

    chunks = make_chunk_records(doc["text"], doc["filename"])

    print("TOTAL CHUNKS:", len(chunks))
    print("-" * 80)

    for chunk in chunks[:3]:
        print(f"Chunk {chunk['chunk_index']}")
        print(chunk["content"][:500])
        print()