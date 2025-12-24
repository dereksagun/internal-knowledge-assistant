from src.core.container import Deps

def build_citations(chosen, deps: Deps):
  citations = []
  for pid, score, hits in chosen:
    rec = deps.parent_db.get_record(pid)
    chunks = []
    for h, _ in hits:
      chunks.append({
        "chunk_id": h.metadata["chunk_id"],
        "section": h.metadata.get("section"),
        "title": h.metadata["title"]
      })
    citations.append({
        "doc_title": rec["doc_title"],
        "source_path": rec["source_path"],
        "parent_id": pid,
        "chunks": chunks
    })
  
  return citations