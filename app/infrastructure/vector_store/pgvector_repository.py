import psycopg2
from typing import List
from app.domain.services import VectorRepository
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class PgVectorRepository(VectorRepository):

    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

    # Infrastructure-specific helper
    def _to_pgvector(self, embedding: List[float]) -> str:
        return "[" + ",".join(str(x) for x in embedding) + "]"

    def save(self, chunk_id: str, content: str, embedding: List[float]) -> None:
        vector_str = self._to_pgvector(embedding)

        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO document_chunks (id, content, embedding)
                VALUES (%s, %s, %s::vector)
                """,
                (chunk_id, content, vector_str),
            )
            self.conn.commit()

    def similarity_search(self, embedding: List[float], k: int):
        vector_str = self._to_pgvector(embedding)

        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, content
                FROM document_chunks
                ORDER BY embedding <-> %s::vector
                LIMIT %s
                """,
                (vector_str, k),
            )
            return cur.fetchall()

