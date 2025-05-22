from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI model
llm = AzureChatOpenAI(
    azure_deployment="gpt-4",
    openai_api_version="2023-05-15",
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    temperature=0.7
)

# Create a template with history placeholder
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Respond with humor when appropriate."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Set up memory
memory = ConversationBufferMemory(return_messages=True, memory_key="history")

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=template,
    memory=memory,
    verbose=True
)

# Interactive chat loop
if __name__ == "__main__":
    print("Chat with the AI (type 'exit' to quit)")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        response = conversation.invoke({"input": user_input})
        print(response["response"])