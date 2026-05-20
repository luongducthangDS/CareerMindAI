"""
ChromaDB vector store — optional feature.
If chromadb / onnxruntime fails (e.g. RAM limit on free hosting),
the app continues normally without saving history.
"""

import os
import logging

logger = logging.getLogger(__name__)

_collection = None
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
_available = True  # set False if init fails


def _get_collection():
    global _collection, _available
    if not _available:
        return None
    if _collection is not None:
        return _collection
    try:
        import chromadb
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(
            name="cv_store",
            embedding_function=DefaultEmbeddingFunction(),
        )
        return _collection
    except Exception as e:
        logger.warning(f"ChromaDB unavailable, history disabled: {e}")
        _available = False
        return None


def save_cv(session_id: str, cv_text: str, analysis: str, metadata: dict = None) -> bool:
    col = _get_collection()
    if col is None:
        return False
    try:
        doc = f"CV:\n{cv_text}\n\nANALYSIS:\n{analysis}"
        meta = {"session_id": session_id, **(metadata or {})}
        col.upsert(ids=[session_id], documents=[doc], metadatas=[meta])
        return True
    except Exception as e:
        logger.warning(f"ChromaDB save failed: {e}")
        return False


def get_cv(session_id: str) -> dict | None:
    col = _get_collection()
    if col is None:
        return None
    try:
        results = col.get(ids=[session_id])
        if results["documents"]:
            return {"document": results["documents"][0], "metadata": results["metadatas"][0]}
    except Exception:
        pass
    return None
