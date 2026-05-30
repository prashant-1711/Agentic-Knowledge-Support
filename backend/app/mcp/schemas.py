from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ToolMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0"
    input_schema: Dict[str, Any]


class ToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]


class ToolResponse(BaseModel):
    success: bool
    tool_name: str
    result: Any
    error: Optional[str] = None


class AgentRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    response: str
    tools_used: List[str] = []
    metadata: Optional[Dict[str, Any]] = None