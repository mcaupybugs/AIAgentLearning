from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class MemoryInterface(ABC):
    """
    Abstract base class for memory interfaces.
    """

    @abstractmethod
    def store_message(self, session_id: str, role: str, content: str):
        """
        Store a message in the memory.
        :param session_id: Unique identifier for the session.
        :param role: Role of the message sender (e.g., user, assistant).
        :param content: Content of the message.
        """
        pass

    # @abstractmethod
    # def retrieve_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    #     """
    #     Retrieve messages from the memory.
    #     :param session_id: Unique identifier for the session.
    #     :param limit: Optional limit on the number of messages to retrieve.
    #     :return: List of messages for the given session.
    #     """
    #     pass

    # @abstractmethod
    # def search_by_similarity(self, query: str, session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    #     """
    #     Search for messages similar to the query.
    #     :param query: The query string to search for.
    #     :param session_id: Unique identifier for the session.
    #     :param limit: Optional limit on the number of similar messages to retrieve.
    #     :return: List of similar messages.
    #     """
    #     pass

    # @abstractmethod
    # def get_facts(self, query: str = None, session_id: str = None, max_facts: int = 5) -> List[Dict[str, Any]]:
    #     """
    #     Retrieve facts from the memory.
    #     :param query: Optional query to find relevant facts.
    #     :param session_id: Unique identifier for the session.
    #     :param max_facts: Maximum number of facts to return.
    #     :return: List of facts for the given session.
    #     """
    #     pass