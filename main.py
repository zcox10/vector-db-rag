import os
from huggingface_hub import login
from src.chunk import Chunk
from src.embed_model import EmbedModel
from src.llm_model import LlmModel
from src.prompt import Prompter


def main():
    CODEBASE_DESTINATION_DIR = "../codebase"

    CODEBASE_SOURCE_DIR = "../data/codebase_txt"

    VECTOR_DB_SOURCE_DIR = "../data/vector_db"

    EMBED_MODEL_KWARGS = {
        "model_name": "jinaai/jina-embeddings-v2-base-code",
        "model_kwargs": {"device": "cpu", "trust_remote_code": True},
        "encode_kwargs": {"normalize_embeddings": True},
    }

    LLM_MODEL_KWARGS = {
        "model_id": "meta-llama/Llama-3.2-1B-Instruct",
        "task": "text-generation",
        "device_map": "auto",
        "max_new_tokens": 1000,
    }

    # Login to Huggingface and initialize classes
    login(os.getenv("HUGGINGFACE_TOKEN"))
    em = EmbedModel(EMBED_MODEL_KWARGS)
    ch = Chunk()
    p = Prompter()
    llm = LlmModel(LLM_MODEL_KWARGS)

    # Chunk codebase
    ch.convert_files_to_txt(CODEBASE_DESTINATION_DIR, CODEBASE_SOURCE_DIR)
    documents = ch.chunk_txt_files(CODEBASE_SOURCE_DIR)
    metadata = [doc.metadata for doc in documents]
    ch.generate_metadata(documents)
    # ch.print_n_documents(documents, -1)

    # Defining embedding model parameters
    DOCUMENT_KWARGS = {
        "documents": documents,
        "path": VECTOR_DB_SOURCE_DIR,
        "metadata": metadata,
        "collection_name": "codebase",
        "prefer_grpc": True,
        "hnsw_config": {"ef_construct": 200, "m": 16},
    }
    vectors = em.embed_documents(DOCUMENT_KWARGS)

    print("Test query")
    query = "What is the syntax to import text_splitter using LangChain?"
    found_docs = em.test_search_query(query, 3, vectors)
    context_text = "\n".join([doc.page_content for doc, _ in found_docs])

    p.generate_response(query, llm.model, context_text)


if __name__ == "__main__":
    main()
