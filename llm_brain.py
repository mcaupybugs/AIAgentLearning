import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class AzureChatBot():
    def __init__(self, model_deployment='gpt-4'):
        load_dotenv()
        self.client =  AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key = os.getenv("OPEN_AI_API_KEY"),
        api_version="2024-12-01-preview"
        )
        self.model = model_deployment
    
    def ask(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content