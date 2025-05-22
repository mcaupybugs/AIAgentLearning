from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

memory = ConversationBufferMemory(return_messages=True, memory_key="history")

chain = ConversationChain(
    llm=llm,
    prompt=template,
    memory=memory
)