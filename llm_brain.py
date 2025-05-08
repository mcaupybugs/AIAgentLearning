import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class LLMBrain():
    def __init__(self):
        """Load API key from .env file"""
        load_dotenv()
        self.open_ai_client = AzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key = os.getenv("OPEN_AI_API_KEY"),
            api_version="2024-12-01-preview"
        )

    def chat(self, message):
        """Chat with the AI bot"""
        model_name = "gpt-4o"
        deployment = "gpt-4o"

        response = self.open_ai_client.chat.completions.create(
            model=deployment, # model = "deployment_name".
            messages=message
        )
        
        return response.choices[0].message.content