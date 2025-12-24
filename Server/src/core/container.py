from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from src.tools.parent_db import ParentDB
from src.tools.ingest_docs import ingest_docs

@dataclass
class Deps:
    embedder: Any
    vector_store: Chroma
    llm: ChatOllama
    parent_db: ParentDB
    
@lru_cache(maxsize=1)
def get_deps() -> Deps:
  embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
  vector_store = Chroma(
    collection_name="InternalCompanyVectorDB",
    embedding_function=embedder,

  )
  llm = ChatOllama(
    model="mistral",
    validate_model_on_init=True
  )
  parent_db = ParentDB()

  ingest_docs(
    Path.cwd() / "docs",
    parent_db=parent_db,
    vector_store=vector_store
  )

  return Deps(embedder, vector_store, llm, parent_db)