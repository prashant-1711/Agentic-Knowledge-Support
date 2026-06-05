from app.mcp.schemas import ToolRequest, ToolResponse


class ToolExecutor:

    def __init__(self, registry):

        self.registry = registry

    async def execute(
        self,
        tool_request: ToolRequest
    ) -> ToolResponse:

        tool = self.registry.get_tool(
            tool_request.tool_name
        )

        # Tool not found
        if not tool:

            return ToolResponse(
                success=False,
                tool_name=tool_request.tool_name,
                result=None,
                error="Tool not found"
            )

        handler = tool["handler"]

        try:

            # Execute tool
            result = await handler(
                **tool_request.arguments
            )

            return ToolResponse(
                success=True,
                tool_name=tool_request.tool_name,
                result=result
            )

        except Exception as e:

            return ToolResponse(
                success=False,
                tool_name=tool_request.tool_name,
                result=None,
                error=str(e)
            )