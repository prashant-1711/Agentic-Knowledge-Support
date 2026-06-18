import asyncio

from app.tools.rag_search_tool import rag_search_tool


async def main():

    response = await rag_search_tool(
        "What is the leave policy?"
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())