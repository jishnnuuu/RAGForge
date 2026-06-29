import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class GroqClient:

    def __init__(
        self,
        model: str = (
            "llama-3.3-70b-versatile"
        )
    ):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.model = model

    def generate(
        self,
        prompt: str,
        system_prompt: str = None # type: ignore
    ) -> str:

        messages = []
        
        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt
                }
            )
        
        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        if content is None:
            raise ValueError(
                "Groq chat completion returned no message content"
            )

        return content