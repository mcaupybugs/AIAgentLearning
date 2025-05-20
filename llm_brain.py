import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from memory.memory_interface import MemoryInterface
from typing import Optional, List, Dict
import uuid

class LLMBrain():
    def __init__(self, memory_system: Optional[MemoryInterface] = None, 
                 max_tokens: int = 1000, 
                 fact_max_tokens: int = 500):
        """Initialize the LLMBrain with an optional memory system.
        
        Args:
            memory_system: Optional memory system for storing and retrieving messages
            max_tokens: Maximum number of tokens for the main chat response
            fact_max_tokens: Maximum number of tokens for the fact extraction response
        """
        load_dotenv()
        self.open_ai_client = AsyncAzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key = os.getenv("OPEN_AI_API_KEY"),
            api_version="2024-12-01-preview"
        )
        self.memory = memory_system
        self.model_name = "gpt-4o"
        self.deployment = "gpt-4o"
        self.max_tokens = max_tokens
        self.fact_max_tokens = fact_max_tokens
            

    # TODO: (Optional) Check what are the messages getting saved in the memory
    async def chat(self, message: List[Dict[str, str]], session_id: Optional[str] = None) -> str:
        """Chat with the AI bot and optionally store the message in memory."""
        if session_id is None:
            session_id = str(uuid.uuid4())

        augmented_messages = message.copy()

        # Get response from LLM
        response = await self.open_ai_client.chat.completions.create(
            model=self.deployment,
            messages=augmented_messages,
            max_tokens=self.max_tokens
        )

        response_content = response.choices[0].message.content
        return response_content


    async def store_messages(self, session_id: str, messages: List[Dict[str, str]]):
        """Store messages in the memory system."""
        # Store the message in memory

        for msg in messages:
            self.memory.store_message(
                session_id=session_id,
                role=msg["role"],
                content=msg["content"]
            )