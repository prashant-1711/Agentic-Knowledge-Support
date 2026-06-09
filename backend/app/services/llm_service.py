import os

import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


class LLMService:

    def __init__(self):

        # Load API key
        api_key = os.getenv("GEMINI_API_KEY")

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Initialize model
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash"
        )

    async def generate_response(
        self,
        prompt: str
    ) -> str:

        response = self.model.generate_content(
            prompt
        )

        return response.text