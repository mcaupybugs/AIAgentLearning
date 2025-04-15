import os
from dotenv import load_dotenv
from openai import AzureOpenAI

model_name = 'gpt-4o'
deployment = 'gpt-4'

def load_api_key():
    """Load API key from .env file"""
    load_dotenv()

def create_openai_model():
    """OpenAI model creation logic."""
    open_ai_client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key = os.getenv("OPEN_AI_API_KEY"),
        api_version="2024-12-01-preview"
    )

    return open_ai_client

def chat(client):
    """Chat with the AI bot"""
    response = client.chat.completions.create(
    model="gpt-35-turbo", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

    print(response.choices[0].message.content)
def main():
    try:
        load_api_key()

        open_ai_client = create_openai_model()
        chat(open_ai_client)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()