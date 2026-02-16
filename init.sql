CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks(
	id UUID PRIMARY KEY,
	content TEXT NOT NULL,
	embedding VECTOR(384) NOT NULL
);

CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ANALYZE document_chunks;
