from sqlalchemy import select
from app.db import SessionLocal
from app.models import Chunk, Document
from app.ingest.embedder import get_embedding


def search_chunks(query: str, top_k: int = 5):
    db = SessionLocal()
    print("\n🔍 Query:", query)
    try:
        query_embedding = get_embedding(
            query,
            task_type="retrieval_query",
            output_dimensionality=768,
        )

        distance = Chunk.embedding.cosine_distance(query_embedding).label("distance")

        stmt = (
            select(
                Chunk.id,
                Document.filename,
                Chunk.chunk_index,
                Chunk.content,
                distance,
            )
            .join(Document, Chunk.document_id == Document.id)
            .order_by(distance)
            .limit(top_k)
        )

        rows = db.execute(stmt).all()

        results = []
        for row in rows:
            results.append(
                {
                    "chunk_id": row.id,
                    "filename": row.filename,
                    "chunk_index": row.chunk_index,
                    "content": row.content,
                    "distance": float(row.distance),
                }
            )

        return results

    finally:
        db.close()