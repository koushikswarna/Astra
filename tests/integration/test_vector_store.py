"""Integration tests for ChromaDB vector store."""

import pytest


class TestVectorStore:
    def test_add_and_query(self, tmp_path):
        from astra.storage.vector_store import VectorStore

        store = VectorStore(persist_dir=tmp_path / "chroma", collection_name="test")

        # create a simple embedding (normally comes from sentence-transformers)
        fake_embedding = [0.1] * 384  # MiniLM dimension
        doc_id = store.add("test document", fake_embedding, {"source": "test"})
        assert doc_id.startswith("mem_")

        # query with the same embedding should find it
        results = store.query(fake_embedding, n_results=1)
        assert len(results) == 1
        assert results[0] == "test document"

    def test_count(self, tmp_path):
        from astra.storage.vector_store import VectorStore

        store = VectorStore(persist_dir=tmp_path / "chroma2", collection_name="test2")
        assert store.count == 0

        store.add("doc1", [0.1] * 384)
        assert store.count == 1

    def test_clear(self, tmp_path):
        from astra.storage.vector_store import VectorStore

        store = VectorStore(persist_dir=tmp_path / "chroma3", collection_name="test3")
        store.add("doc1", [0.1] * 384)
        store.add("doc2", [0.2] * 384)
        assert store.count == 2

        store.clear()
        assert store.count == 0
