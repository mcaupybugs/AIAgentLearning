import os
from semantic_kernel import Kernel
from semantic_kernel.memory.memory_record import MemoryRecord

from main import initialize_chat_service
from dotenv import load_dotenv
from openai import AzureOpenAI

class LLMBrain():
    def __init__(self):
        load_dotenv()
        kernel = Kernel()
        initialize_chat_service(kernel=kernel)

        with open("context.txt", "r") as f:
            content = f.read()
            kernel.memory.store(MemoryRecord(text=content))

    