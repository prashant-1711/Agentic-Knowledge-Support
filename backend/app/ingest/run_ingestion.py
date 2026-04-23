from app.db import SessionLocal
from app.ingest.pdf_loader import load_pdfs_from_folder
from app.ingest.chunker import make_chunk_records
from app.ingest.store import store_document, store_chunks


DATA_PATH = r"D:\Agentic Knowledge Support\data\sample_doc"


def run():
    db = SessionLocal()

    docs = load_pdfs_from_folder(DATA_PATH)

    for doc in docs:
        print(f"\n📄 Processing: {doc['filename']}")

        # 1. store document
        db_doc = store_document(db, doc["filename"])

        # 2. chunk text
        chunks = make_chunk_records(doc["text"], doc["filename"])

        print(f"🔹 Total chunks: {len(chunks)}")

        # 3. store chunks
        store_chunks(db, db_doc.id, chunks)

    db.close()
    print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    run()