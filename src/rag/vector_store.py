from __future__ import annotations

from pathlib import Path
from typing import Any
import chromadb
from rag.parser import parse_policy_markdown


class ChromaPolicyStore:
    """Student scaffold for the real Chroma-backed policy index."""

    def __init__(
        self,
        persist_directory: Path,
        embedding_model: Any,
        collection_name: str = "policy_chunks",
    ) -> None:
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        
        # Ensure the directory exists
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def ensure_index(self, markdown_path: Path) -> None:
        if self.collection.count() == 0:
            self.rebuild(markdown_path)

    def rebuild(self, markdown_path: Path) -> None:
        # Clear collection if exists
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.create_collection(name=self.collection_name)
        
        markdown_text = markdown_path.read_text(encoding="utf-8")
        chunks = parse_policy_markdown(markdown_text)
        
        if not chunks:
            return
            
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            ids.append(f"policy-{i}")
            documents.append(chunk["rendered_text"])
            metadatas.append({
                "section_h2": chunk["section_h2"],
                "section_h3": chunk["section_h3"],
                "citation": chunk["citation"]
            })
            
        embeddings = self.embedding_model.embed_documents(documents)
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def search(self, query: str, top_k: int = 4) -> list[dict[str, Any]]:
        query_embedding = self.embedding_model.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        hits = []
        if not results or not results.get("ids"):
            return hits
            
        ids = results["ids"][0]
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(ids)
        metadatas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(ids)
        documents = results["documents"][0] if results.get("documents") else [""] * len(ids)
        
        for idx in range(len(ids)):
            hits.append({
                "id": ids[idx],
                "citation": metadatas[idx].get("citation", "") if metadatas[idx] else "",
                "content": documents[idx],
                "distance": distances[idx],
                "section_h2": metadatas[idx].get("section_h2", "") if metadatas[idx] else "",
                "section_h3": metadatas[idx].get("section_h3", "") if metadatas[idx] else "",
            })
        return hits

