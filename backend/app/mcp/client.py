from app.mcp.registry import ToolRegistry
from app.mcp.schemas import ToolMetadata
from app.mcp.tool_executor import ToolExecutor

from app.agents.tool_router import ToolRouter
from app.agents.orchestrator import AgentOrchestrator

from app.tools.rag_search_tool import rag_search_tool


def get_orchestrator():

    registry = ToolRegistry()

    metadata = ToolMetadata(
        name="rag_search_tool",
        description="Search internal knowledge documents",
        input_schema={
            "query": "string"
        }
    )

    registry.register_tool(
        metadata=metadata,
        handler=rag_search_tool
    )

    router = ToolRouter(registry)

    executor = ToolExecutor(registry)

    orchestrator = AgentOrchestrator(
        router=router,
        executor=executor
    )

    return orchestrator