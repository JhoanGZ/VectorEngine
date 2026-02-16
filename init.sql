-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
	id UUID PRIMARY KEY,
	content TEXT NOT NULL,
	embedding VECTOR(384)
);

-- Create IVFFLAT index for cosine similarity
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE tablename = 'document_chunks'
        AND indexname = 'document_chunks_embedding_idx'
    ) THEN
        CREATE INDEX document_chunks_embedding_idx
        ON document_chunks
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    END IF;
END $$;

-- Update planner statistics
ANALYZE document_chunks;
