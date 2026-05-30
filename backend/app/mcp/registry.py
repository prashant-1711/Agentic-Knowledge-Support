from typing import Dict, Callable

from mcp.schemas import ToolMetadata


class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, dict] = {}

    def register_tool(
        self,
        metadata: ToolMetadata,
        handler: Callable
    ):
        """
        Register a new tool with its metadata and execution handler.
        """

        self.tools[metadata.name] = {
            "metadata": metadata,
            "handler": handler
        }

    def get_tool(self, tool_name: str):

        return self.tools.get(tool_name)

    def list_tools(self):

        return [
            tool_data["metadata"]
            for tool_data in self.tools.values()
        ]

    def tool_exists(self, tool_name: str) -> bool:

        return tool_name in self.tools