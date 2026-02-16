from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    """
    Contract for embedding generation. 
    Domain depens on this abstraction only.
    """

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        pass

class VectorRepository(ABC):
    """
    Contract for vector storage and retrieval
    """

    @abstractmethod
    def save(self, chunk_id: str, content: str, embedding: List[float]) -> None:
        pass

    @abstractmethod
    def similarity_search(self, embedding: List[float], k: int):
        pass


class LLMProvider(ABC):
    """
    Contract for LLM-based generation
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


    
