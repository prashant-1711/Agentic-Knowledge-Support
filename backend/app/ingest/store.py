#Updated storing logic to include embedding generation for each chunk. This ensures that when we store chunks in the database,
# we also compute and save their embeddings, which are essential for later retrieval and similarity searches.

from sqlalchemy.orm import Session
from app.models import Document, Chunk
from app.ingest.embedder import get_embedding


def store_document(db: Session, filename: str):
    doc = Document(filename=filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def store_chunks(db: Session, document_id: str, chunks: list):
    chunk_objects = []

    for chunk in chunks:
        print(f"🔹 Embedding chunk {chunk['chunk_index']}")

        embedding = get_embedding(chunk["content"])

        chunk_obj = Chunk(
            document_id=document_id,
            content=chunk["content"],
            chunk_index=chunk["chunk_index"],
            embedding=embedding
        )

        chunk_objects.append(chunk_obj)

    db.add_all(chunk_objects)
    db.commit()
    
    
    # from sqlalchemy.orm import Session
# from app.models import Document, Chunk


# def store_document(db: Session, filename: str):
#     doc = Document(filename=filename)
#     db.add(doc)
#     db.commit()
#     db.refresh(doc)
#     return doc


# def store_chunks(db: Session, document_id: str, chunks: list):
#     chunk_objects = []

#     for chunk in chunks:
#         chunk_obj = Chunk(
#             document_id=document_id,
#             content=chunk["content"],
#             chunk_index=chunk["chunk_index"]
#         )
#         chunk_objects.append(chunk_obj)

#     db.add_all(chunk_objects)
#     db.commit() 
