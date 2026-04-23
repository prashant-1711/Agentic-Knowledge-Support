from sqlalchemy.orm import Session
from app.models import Document, Chunk


def store_document(db: Session, filename: str):
    doc = Document(filename=filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def store_chunks(db: Session, document_id: str, chunks: list):
    chunk_objects = []

    for chunk in chunks:
        chunk_obj = Chunk(
            document_id=document_id,
            content=chunk["content"],
            chunk_index=chunk["chunk_index"]
        )
        chunk_objects.append(chunk_obj)

    db.add_all(chunk_objects)
    db.commit() 