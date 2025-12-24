import uuid
from pathlib import Path
from datetime import date

from langchain_chroma import Chroma

from src.utils.chunking import split_markdown
from src.utils.filesystem import find_all_files_paths
from src.tools.document_loaders import load_docx
from src.tools.metadata import enrich_chunk
from src.tools.parent_db import ParentDB

def ingest_docs(docs_path: Path, parent_db: ParentDB, vector_store: Chroma):
  paths = find_all_files_paths(docs_path, [])
  docs = []
  for path in paths:
    content = load_docx(path)
    parent_id = str(uuid.uuid4())

    parent_db.add_document(parent_id, {
        "parent_id": parent_id,
        "doc_title": path.name,
        "source_path": str(path),
        "content": content,
        "last_updated": date.today().strftime("%Y-%m-%d"),
    })

    chunks = split_markdown(content)
    for doc in chunks:
        enrich_chunk(doc, parent_id=parent_id, path=path)
        docs.append(doc)
  
  vector_store.add_documents(docs)
