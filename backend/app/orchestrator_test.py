import asyncio
from urllib import response

from app.mcp.registry import ToolRegistry
from app.mcp.schemas import ToolMetadata
from app.mcp.tool_executor import ToolExecutor

from app.agents.tool_router import ToolRouter
from app.agents.orchestrator import AgentOrchestrator


# Fake RAG tool
# async def rag_search_tool(query: str):

#     return f"RAG Result for: {query}"

#real rag tool
from app.tools.rag_search_tool import rag_search_tool

async def main():

    # Create registry
    registry = ToolRegistry()

    # Register fake RAG tool
    metadata = ToolMetadata(
        name="rag_search_tool",
        description="Search internal knowledge base",
        input_schema={
            "query": "string"
        }
    )

    registry.register_tool(
        metadata=metadata,
        handler=rag_search_tool
    )

    # Create router
    router = ToolRouter(registry)

    # Create executor
    executor = ToolExecutor(registry)

    # Create orchestrator
    orchestrator = AgentOrchestrator(
        router=router,
        executor=executor
    )

    # Test query
    response = await orchestrator.process_query(
        "What is the leave policy?"
    )

    print("\n=== ANSWER ===\n")
    print(response.response)

    print("\n=== TOOLS USED ===\n")
    print(response.tools_used)

    print("\n=== SOURCES ===\n")

    for source in response.metadata["sources"]:
        print(
        f"{source['filename']} "
        f"(chunk {source['chunk_index']})"
        )


if __name__ == "__main__":

    asyncio.run(main())