import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from llm_brain import LLMBrain

def main():
    try:
        # Initialize the LLMBrain
        llm_brain = LLMBrain()
        
        while True:
            query = input("How can I help you sir?\n")
            message = [
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            # Use the chat method from LLMBrain
            response = llm_brain.chat(message)
            print(response)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()