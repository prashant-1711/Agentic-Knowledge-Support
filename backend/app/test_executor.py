import asyncio

from app.mcp.registry import ToolRegistry
from app.mcp.schemas import ToolMetadata, ToolRequest
from app.mcp.tool_executor import ToolExecutor


# Fake async tool
async def test_tool(query: str):

    return f"Received Query: {query}"


async def main():

    # Create registry
    registry = ToolRegistry()

    # Create tool metadata
    metadata = ToolMetadata(
        name="test_tool",
        description="Simple test tool",
        input_schema={
            "query": "string"
        }
    )

    # Register tool
    registry.register_tool(
        metadata=metadata,
        handler=test_tool
    )

    # Create executor
    executor = ToolExecutor(registry)

    # Create request
    request = ToolRequest(
        tool_name="test_tool",
        arguments={
            "query": "hello MCP"
        }
    )

    # Execute tool
    response = await executor.execute(request)

    print(response)


if __name__ == "__main__":

    asyncio.run(main())