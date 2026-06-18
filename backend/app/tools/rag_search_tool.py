from app.services.rag_pipeline import generate_answer


async def rag_search_tool(query: str):

    result = generate_answer(query)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }