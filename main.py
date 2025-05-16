import os
# Set environment variable before importing any libraries that might use tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import uuid
import asyncio
from dotenv import load_dotenv
from llm_brain import LLMBrain
from memory.sqlite_memory import SQLiteMemory

async def main():
    try:
        # Initialize the LLMBrain
        session_id = str(uuid.uuid4())
        memory = SQLiteMemory()

        # Initialize with conservative token limits to avoid rate limiting
        llm_brain = LLMBrain(
            memory_system=memory,
            max_tokens=500,  # Limit main responses to 500 tokens
            fact_max_tokens=200  # Limit fact extraction to 200 tokens
        )

        print("Welcome to the LLM Brain! Type 'exit' to quit.")
        conversation_history = []

        while True:
            query = input("How can I help you sir?\n")
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            conversation_history.append({
                "role": "user",
                "content": query
            })

            # Use the chat method from LLMBrain
            print("Processing your request...")
            response = await llm_brain.chat(conversation_history, session_id=session_id)
            print(response)
            
            conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Keep history manageable
            if len(conversation_history) > 10:
                # Keep only the last 10 messages
                conversation_history = conversation_history[-10:]

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())