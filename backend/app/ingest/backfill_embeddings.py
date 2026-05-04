import time
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Chunk
from app.ingest.embedder import get_embedding

BATCH_SIZE = 10
SLEEP_SECONDS = 1


def run():
    db = SessionLocal()
    try:
        chunks = (
            db.execute(
                select(Chunk)
                .where(Chunk.embedding.is_(None))
                .order_by(Chunk.id)
            )
            .scalars()
            .all()
        )

        print(f"Found {len(chunks)} chunks without embeddings.")

        for i, chunk in enumerate(chunks, start=1):
            print(f"Embedding chunk {i}/{len(chunks)} | {chunk.id}")
            chunk.embedding = get_embedding(
                chunk.content,
                task_type="retrieval_document",
                output_dimensionality=768,
            )

            if i % BATCH_SIZE == 0:
                db.commit()
                print(f"Committed batch ending at {i}")
                time.sleep(SLEEP_SECONDS)

        db.commit()
        print("✅ Embedding backfill complete")

    finally:
        db.close()


if __name__ == "__main__":
    run()