from typing import Dict, Any, List, Tuple
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document


class EmbedModel:
    """
    A class for embedding documents and performing vector search.
    """

    def __init__(self, model_kwargs: Dict[str, Any] = None) -> None:
        self.model = HuggingFaceEmbeddings(**model_kwargs)

    def embed_documents(self, document_kwargs: Dict[str, Any]) -> Qdrant:
        """
        Embeds documents and stores them in a vector store.
        """
        if not document_kwargs.get("documents"):
            raise ValueError("The 'documents' key must be provided in document_kwargs.")

        # Defines embedding model to use for vector embeddings
        document_kwargs["embedding"] = self.model
        return Qdrant.from_documents(**document_kwargs)

    def pretty_print_docs(self, found_docs: List[Tuple[Document, float]]) -> None:
        """
        Prints context documents and their similarity scores.
        """
        print("\n--- Retrieved Documents ---\n")
        for doc, score in found_docs:
            print(f"Score: {score:.4f}")
            print(f"Metadata: {doc.metadata}")
            print("-" * 100)
            print(f"Content:\n{doc.page_content}\n")
        print("--- End of Results ---\n")

    def test_search_query(
        self, query: str, k: int, vectors: Qdrant, print_results: bool = False
    ) -> List[Tuple[Document, float]]:
        """
        Performs a similarity search against the vector store.
        """
        found_docs = vectors.similarity_search_with_score(query, k)
        if print_results:
            self.pretty_print_docs(found_docs)
        return found_docs
