from pathlib import Path
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from src.tools.parent_db import ParentDB
from src.core.container import Deps

def find_parent_docs(retrieved):
  parents: dict[str, List[Tuple[Document, float]]] = {}

  for chunk, dist in retrieved:
    pid = chunk.metadata.get("parent_id")
    parents.setdefault(pid, []).append((chunk, dist))

  for p in parents.items():
    hits = p[1]
    for h in hits:
      print(f"Score: {h[1]} - DOC: {h[0].metadata.get("doc_title")}")
    
  return parents

def find_best_parent_scores(parents: dict[str, List[Tuple[Document, float]]]):
  scored: List[Tuple[str, float, Document]] = []
  for pid, hits in parents.items():
    min_dist = min(dist for _, dist in hits)
    scored.append((pid, min_dist, hits))

  scored.sort(key=lambda x: x[1])
  
  best = scored[0][1]
  delta = 0.32
  max_parents = 2

  chosen = [(pid, score, hits) for pid, score, hits in scored 
            if score <= best + delta][:max_parents]
  return chosen

def get_parent_ids(chosen):
  return [pid for pid, _, _ in chosen]




