from fastapi import FastAPI
from pydantic import BaseModel

from app.mcp.client import get_orchestrator

app = FastAPI()

orchestrator = get_orchestrator()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "RAG API is running"}


@app.post("/ask")
async def ask_question(request: QueryRequest):

    result = await orchestrator.process_query(
        request.query
    )

    return {
        "answer": result.response,
        "tools_used": result.tools_used,
        "metadata": result.metadata
    }