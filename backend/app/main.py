from fastapi import FastAPI
from pydantic import BaseModel

from app.services.rag_pipeline import generate_answer

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "RAG API is running"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    result = generate_answer(request.query)
    return result