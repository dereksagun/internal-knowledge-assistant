from pathlib import Path
import uuid
from datetime import date

def enrich_chunk(doc, parent_id, path):
    doc.metadata.update({
        "source_path": str(path),
        "doc_title": path.name,
        "parent_id": parent_id,
        "chunk_id": str(uuid.uuid4()),
        "last_updated": date.today().strftime("%Y-%m-%d"),
    })