import os
# Set environment variable before importing tokenizers to avoid warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import sqlite3
from memory.memory_interface import MemoryInterface
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

class SQLiteMemory(MemoryInterface):
    def __init__(self, db_path: str = 'agent_memory.db'):
        self.db_path = db_path
        self.db_connection = sqlite3.connect(db_path)
        self.short_term_memory = []
        # self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database and create necessary tables."""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT,
                source_message_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_message_id) REFERENCES messages (id)
            )
        ''')

        self.db_connection.commit()

    def store_message(self, session_id: str, role: str, content: str):
        """Store a message in the short-term memory and database."""
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        self.db_connection.commit()
        # Append to short-term memory for quick access
        self.short_term_memory.append({
            "role": role,
            "content": content,
            "session_id": session_id
        })
        print(f"Stored message: {content}")
        # Limit short-term memory size
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)

    # def retrieve_messages(self, session_id: str, limit: int = None) -> List[Dict[str, Any]]:
    #     """Retrieve messages from the database for a specific session."""
    #     cursor = self.db_connection.cursor()
    #     query = "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id DESC"
    #     params = [session_id]

    #     if limit:
    #         query += " LIMIT ?"
    #         params.append(limit)

    #     cursor.execute(query, params)
    #     rows = cursor.fetchall()

    #     return [{"role": row[0], "content": row[1]} for row in rows]

    # def search_by_similarity(self, query: str, session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    #     """Search for messages similar to the query in the database."""
    #     query_embedding = self.embedding_model.encode(query)
    #     cursor = self.db_connection.cursor()
    #     cursor.execute("SELECT id, session_id, role, content, embedding FROM messages WHERE session_id = ?", (session_id,))

    #     result = []
    #     for row in cursor.fetchall():
    #         id, session_id, role, content, embedding_bytes = row
    #         # calculating the cosine similarity
    #         embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
    #         similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
    #         result.append({
    #             "id": id,
    #             "session_id": session_id,
    #             "role": role,
    #             "content": content,
    #             "similarity": similarity
    #         })

    #     # Sort by similarity and limit results
    #     result.sort(key=lambda x: x["similarity"], reverse=True)
    #     return result[:limit]
    
    # def get_facts(self, query: str = None, session_id: str = None, max_facts: int = 5) -> List[Dict[str, Any]]:
    #     """
    #     Retrieve facts from the memory.
    #     :param query: Optional query to find relevant facts.
    #     :param session_id: Unique identifier for the session.
    #     :param max_facts: Maximum number of facts to return.
    #     :return: List of facts for the given session.
    #     """
    #     cursor = self.db_connection.cursor()
        
    #     # First get stored facts from the database (limited to improve efficiency)
    #     if session_id:
    #         cursor.execute("""
    #             SELECT f.fact, f.confidence 
    #             FROM facts f
    #             JOIN messages m ON f.source_message_id = m.id
    #             WHERE m.session_id = ?
    #             ORDER BY f.confidence DESC
    #             LIMIT ?
    #         """, (session_id, max_facts))
    #     else:
    #         cursor.execute("""
    #             SELECT fact, confidence FROM facts
    #             ORDER BY confidence DESC
    #             LIMIT ?
    #         """, (max_facts,))
            
    #     stored_facts = [{"fact": row[0], "confidence": row[1]} for row in cursor.fetchall()]
        
    #     # If we have a query and session_id, get a limited number of similar messages
    #     facts_from_messages = []
    #     if query and session_id:
    #         # Limit the number of similar messages to search for
    #         similar_messages = self.search_by_similarity(query, session_id, limit=2)
    #         facts_from_messages = [
    #             {"fact": msg["content"], "confidence": msg["similarity"]} 
    #             for msg in similar_messages
    #         ]
        
    #     return stored_facts + facts_from_messages
    
    # def store_fact(self, fact: str, source_message_id: int, confidence: float =0.9)-> None:
    #     """Store a fact in the database."""
    #     cursor = self.db_connection.cursor()
    #     print(f"Storing fact: {fact} with confidence: {confidence}")
    #     cursor.execute(
    #         "INSERT INTO facts (fact, source_message_id, confidence) VALUES (?, ?, ?)",
    #         (fact, source_message_id, confidence)
    #     )
    #     self.db_connection.commit()

    