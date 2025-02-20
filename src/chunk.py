from pathlib import Path
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class Chunk:
    """
    A class to handle document processing including:
        - File conversion to text
        - Text chunking
        - Metadata generation
        - Document inspection
    """

    def __init__(self) -> None:
        pass

    def convert_files_to_txt(self, src_dir: str, dst_dir: str) -> None:
        """
        Converts files from the source dir into `.txt` format and saves them to destination directory.
        `.jpg` files are ignored.
        """
        src_path = Path(src_dir)
        dst_path = Path(dst_dir)

        # Create destination dir if does not exist
        dst_path.mkdir(parents=True, exist_ok=True)

        # Walk through source dir and process each file
        for file_path in src_path.rglob("*"):
            if file_path.is_file() and not file_path.suffix.lower() == ".jpg":
                relative_path = file_path.relative_to(src_path)
                new_file_path = dst_path / relative_path.with_suffix(".txt")

                # Ensure dir structure exists in the destination dir
                new_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Read and convert file encoded text
                try:
                    data = file_path.read_text(encoding="utf-8")
                except UnicodeDecodeError as e:
                    print(f"Failed to decode the file: {file_path}. Error: {e}")
                    continue

                # Write converted text file
                try:
                    new_file_path.write_text(data, encoding="utf-8")
                except IOError as e:
                    print(f"Failed to write to {new_file_path}. Error: {e}")

    def chunk_txt_files(
        self, src_dir: str, chunk_size: int = 1500, chunk_overlap: int = 150
    ) -> List[Document]:
        """
        Splits text documents into smaller chunks for efficient processing.
        """
        loader = DirectoryLoader(src_dir, show_progress=True, loader_cls=TextLoader)
        try:
            repo_files = loader.load()
            print(f"Number of files loaded: {len(repo_files)}")
        except Exception as e:
            raise RuntimeError(f"Failed to load documents from {src_dir}. Error: {e}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        documents = text_splitter.split_documents(repo_files)
        print(f"Number of document chunks generated: {len(documents)}")

        return documents

    def generate_metadata(self, documents: List[Document]) -> List[Document]:
        """
        Generates metadata for each document by removing the `.txt` extension from source paths.
        """
        for doc in documents:
            source_path = doc.metadata.get("source", "")
            if source_path.endswith(".txt"):
                doc.metadata["source"] = source_path.replace(".txt", "")

        return documents

    def print_n_documents(self, documents: List[Document], n: int = -1) -> None:
        """
        Prints the content of up to `n` documents. If `n` is -1, all documents are printed.
        """
        num_docs = len(documents) if n == -1 else min(n, len(documents))
        print(f"\nPrinting {num_docs} document(s)...\n")

        for doc in documents[:num_docs]:
            print("=" * 100)
            print(f"Document Metadata: {doc.metadata}")
            print("-" * 100)
            print(f"{doc.page_content}\n")
        print("=" * 100)
