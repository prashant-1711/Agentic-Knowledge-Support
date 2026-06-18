from unittest import result

from app.mcp.schemas import (
    AgentResponse,
    ToolRequest
)


class AgentOrchestrator:

    def __init__(
        self,
        router,
        executor
    ):

        self.router = router
        self.executor = executor

    async def process_query(
        self,
        query: str
    ) -> AgentResponse:

        # Step 1 - Decide tool
        selected_tool = self.router.route(query)

        # Step 2 - No tool needed
        if selected_tool == "llm":

            return AgentResponse(
                response=f"No suitable tool found for: {query}",
                tools_used=[]
            )

        # Step 3 - Create tool request
        tool_request = ToolRequest(
            tool_name=selected_tool,
            arguments={
                "query": query
            }
        )

        # Step 4 - Execute tool
        tool_response = await self.executor.execute(
            tool_request
        )

        # Step 5 - Handle failures
        if not tool_response.success:

            return AgentResponse(
                response=f"Tool execution failed: {tool_response.error}",
                tools_used=[selected_tool]
            )

        # Step 6 - Return final response
        result = tool_response.result

        return AgentResponse(
            response=result["answer"],
            tools_used=[selected_tool],
            metadata={
            "sources": result["sources"]
                    }
)