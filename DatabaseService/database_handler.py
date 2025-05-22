from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings

class DatabaseHandler:
    def __init__(self, collection_name, persist_directory = "./chroma_db"):
        self.embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",  # Update to your embedding deployment
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"))

        self.vectordb = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
            client_settings={"chroma_server_host": "localhost", "chroma_server_port": 8000})

    def connect(self):
        # Simulate a database connection
        self.connection = f"Connected to {self.db_name}"

    def disconnect(self):
        # Simulate closing the database connection
        self.connection = None

    def execute_query(self, query):
        if self.connection:
            return f"Executing query: {query}"
        else:
            return "No database connection established."