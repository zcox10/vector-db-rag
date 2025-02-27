import os
import time
from tqdm import tqdm
from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Chunk:

    def __init__(self) -> None:
        self.total_chunks = 0
        self.total_lines = 0
        self.total_size_bytes = 0

    def _get_files(self, root_dir: str, file_extensions: List[str]) -> List[str]:
        """
        Recursively finds files with specified extensions in the root directory.
        """
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith(tuple(ext.lower() for ext in file_extensions)):
                    yield os.path.join(dirpath, filename)

    def chunk_repo(
        self, repo_path: str, language: str = None, chunk_size: int = 1500, chunk_overlap: int = 150,
        output_dir: str = None, file_extensions: List[str] = [".cc", ".h"]
    ) -> List[Document]:
        """
        Partition files from the given repository into smaller chunks.
        Supports language-specific splitting and saves chunks to files.
        """
        # Reset stats
        self.total_chunks = 0
        self.total_lines = 0
        self.total_size_bytes = 0

        # Configure text splitter
        if language:
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=language, chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

        documents = []
        repo_path = Path(repo_path)
        file_list = list(self._get_files(repo_path, file_extensions))
        total_files = len(file_list)

        with tqdm(total=total_files, desc="Chunking repository", unit="file") as pbar:
            for file_path in self._get_files(repo_path, file_extensions):
                # Get file size
                file_size = os.path.getsize(file_path)
                self.total_size_bytes += file_size

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Failed to read {file_path}. Error: {e}")
                    continue

                lines_of_code = len(content.splitlines())
                self.total_lines += lines_of_code

                # Split into chunks
                chunks = text_splitter.split_text(content)
                self.total_chunks += len(chunks)
                relative_path = Path(file_path).relative_to(repo_path)
            
                if output_dir:
                    chunked_subdir = Path(output_dir) / relative_path.parent
                    chunked_subdir.mkdir(parents=True, exist_ok=True)
                    base_name = Path(file_path).stem
                    for i, chunk in enumerate(chunks):
                        chunk_filename = chunked_subdir / f"{base_name}_chunk_{i}.txt"
                        try:
                            chunk_filename.write_text(chunk, encoding="utf-8")
                        except IOError as e:
                            print(f"Failed to write to {chunk_filename}. Error: {e}")

                # Convert chunks to Document objects
                for i, chunk in enumerate(chunks):
                    new_doc = Document(
                        page_content=chunk,
                        metadata={"source": str(file_path), "chunk_id": i}
                    )
                    documents.append(new_doc)
                
                pbar.update(1)

        self._print_stats()
        return documents

    def generate_metadata(self, documents: List[Document]) -> List[Document]:
        """
        Generates metadata for each document. Optionally modifies source paths if needed.
        """
        for doc in documents:
            # No .txt extension to remove since we work with original files
            doc.metadata["source"] = doc.metadata.get("source", "")
        return documents

    def _print_stats(self) -> None:
        """
        Prints statistics about the chunking process.
        """
        total_size_kb = self.total_size_bytes / 1024
        total_size_mb = total_size_kb / 1024
        total_size_gb = total_size_mb / 1024
        print(f"\nTotal chunks created: {self.total_chunks}")
        print(f"Total lines of code: {self.total_lines}")
        print(f"Total size of chunked files: {self.total_size_bytes} bytes "
              f"({total_size_kb:.2f} KB, {total_size_mb:.2f} MB, {total_size_gb:.2f} GB)")

if __name__ == "__main__":
    chunker = Chunk()

    repo_path = "linux"
    output_dir = "chunked_linux"

    start_time = time.time()

    documents = chunker.chunk_repo(
        repo_path=repo_path,
        language="c",
        chunk_size=2000,
        chunk_overlap=200,
        output_dir=output_dir,
        file_extensions=[".c", ".h"]
    )

    end_time = time.time()
    print(f"\nChunking process completed in {end_time - start_time:.2f} seconds.")