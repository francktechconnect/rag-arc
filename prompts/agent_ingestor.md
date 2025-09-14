# Placeholder for prompts/agent_ingestor.md
Role: Ingestion Agent
Goal: Build/refresh a ChromaDB index from DATA_DIR.
Tools: text splitter, embeddings, chroma client
Steps: enumerate files; extract text; chunk; embed; upsert with stable ids; record metadatas (source, title, chunk_idx). Return {docs_indexed, chunks}
Done when: Chroma contains ≥ one collection with ≥ one document; return counts.