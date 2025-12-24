from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.tools.parent_db import ParentDB
from src.tools.ingest_docs import ingest_docs
from langchain_openai import ChatOpenAI

@dataclass
class Deps:
    embedder: Any
    vector_store: Chroma
    llm: ChatOpenAI
    parent_db: ParentDB
    
@lru_cache(maxsize=1)
def get_deps() -> Deps:
  embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
  vector_store = Chroma(
    collection_name="InternalCompanyVectorDB",
    embedding_function=embedder,

  )
  llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
  )
  parent_db = ParentDB()

  if(vector_store._collection.count() == 0):
    ingest_docs(
      Path.cwd() / "docs",
      parent_db=parent_db,
      vector_store=vector_store
    )
  
  

  return Deps(embedder, vector_store, llm, parent_db)