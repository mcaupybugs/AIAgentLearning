from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate

class LLMBrain:
    def __init__(self, llm, memory_key="history"):
        self.llm = llm
        self.memory = ConversationBufferMemory(return_messages=True, memory_key=memory_key)
        self.template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Respond with humor when appropriate."),
            MessagesPlaceholder(variable_name=memory_key),
            ("human", "{input}")
        ])
        self.conversation = ConversationChain(
            llm=self.llm,
            prompt=self.template,
            memory=self.memory,
            verbose=True
        )

    def chat(self, user_input):
        response = self.conversation.invoke({"input": user_input})
        return response["response"]