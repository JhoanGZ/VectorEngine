import psycopg2
from typing import List
from app.domain.services import VectorRepository


class PgVectorRepository:

    def __init__(self, host, port, db_name, user, password):
       self.host = host
       self.port = port
       self.db_name = db_name
       self.user = user
       self.password = password

       self.conn = psycopg2.connect(
               host=self.host,
               port=self.port,
               dbname=self.db_name,
               user=self.user,
               password=self.password
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
                SELECT id, content, embedding <-> %s::vector AS score
                FROM document_chunks
                ORDER BY embedding <-> %s::vector
                LIMIT %s
                """,
                (vector_str, vector_str, k),
            )
            rows = cur.fetchall()

        return[        
                {
                    "id": row[0],
                    "content": row[1],
                    "score": row[2]
                }
                for row in rows
        ]



