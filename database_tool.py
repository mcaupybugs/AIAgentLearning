import sqlite3

class MemoryStorage:
    def __init__(self):
        self.db_connection = sqlite3.connect('agent_memory.db')
        self.short_term_memory = [] 
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def store_message(self, session_id, role, content):
        """Store a message in the short-term memory."""
        embedding = self.embedding_model.encode(content)
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content, embedding) VALUES (?, ?, ?, ?)",
            (session_id, role, content, embedding.tobytes())
        )
        self.db_connection.commit()
        # Append to short-term memory for quick access
        self.short_term_memory.append({
            "role": role,
            "content": content
        })