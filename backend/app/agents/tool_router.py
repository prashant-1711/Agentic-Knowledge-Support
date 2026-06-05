class ToolRouter:

    def __init__(self, registry):

        self.registry = registry

    def route(self, query: str) -> str:

        query = query.lower()

        # RAG / document search
        if any(word in query for word in [
            "policy",
            "document",
            "knowledge",
            "leave",
            "guideline",
            "pdf"
        ]):

            if self.registry.tool_exists("rag_search_tool"):
                return "rag_search_tool"

        # SQL / database queries
        if any(word in query for word in [
            "database",
            "employee",
            "record",
            "table",
            "sql"
        ]):

            if self.registry.tool_exists("sql_tool"):
                return "sql_tool"

        # Browser automation
        if any(word in query for word in [
            "browser",
            "website",
            "open",
            "search online"
        ]):

            if self.registry.tool_exists("browser_tool"):
                return "browser_tool"

        # Filesystem operations
        if any(word in query for word in [
            "file",
            "folder",
            "read file",
            "save"
        ]):

            if self.registry.tool_exists("filesystem_tool"):
                return "filesystem_tool"

        # Default fallback
        return "llm"