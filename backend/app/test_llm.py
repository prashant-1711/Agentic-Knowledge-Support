import asyncio

from app.services.llm_service import LLMService


async def main():

    llm = LLMService()

    response = await llm.generate_response(
        "Explain MCP in simple terms"
    )

    print(response)


if __name__ == "__main__":

    asyncio.run(main())