from typing import List
from sentence_transformers import SentenceTransformer
from app.domain.services import EmbeddingProvider


class LocalEmbeddingService(EmbeddingProvider):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
