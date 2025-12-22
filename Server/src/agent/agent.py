from typing import Any, List, Tuple
from langchain.agents import create_agent
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from datetime import date
from langsmith import traceable
from langchain.agents.middleware import AgentState, AgentMiddleware
import pprint
import uuid

from langchain_core.documents import Document

def find_all_files_paths(path: Path, list_of_paths: List[str]):
  """Retrieves the paths of all the files in the starting directory"""
  for child in path.iterdir():
    if child.is_file() and child.name.lower().endswith(".docx"):
      list_of_paths.append(f"{child}")
    elif child.is_dir():
      find_all_files_paths(path / child, list_of_paths)
  return list_of_paths

model = ChatOllama(
  model="mistral",
  validate_model_on_init=True
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


vector_store = Chroma(
  collection_name="InternalCompanyVectorDB",
  embedding_function=embeddings,
)

headers_to_split_on = [
  ("#", "title"),
  ("##", "section"),
  ("###", "subsection"),
] 

markdown_splitter = MarkdownHeaderTextSplitter(
  headers_to_split_on=headers_to_split_on
)

paths = []
find_all_files_paths((Path.cwd() / 'docs'), paths)

parentDB: dict[str, Any] = {}

for path in paths:
  loader = Docx2txtLoader(path)
  document_files = loader.load()
  parent_id = str(uuid.uuid4())
  parentDB[parent_id] = {
    "parent_id": parent_id,
    "doc_title": Path(path).name,
    "source_path": path,
    "content": document_files[0].page_content,
    "last_updated": date.today().strftime("%Y-%m-%d")
    }
  docs = markdown_splitter.split_text(document_files[0].page_content)
  for doc in docs:
    doc.metadata["source_path"] = path
    doc.metadata["last_updated"] = date.today().strftime("%Y-%m-%d")
    doc.metadata["doc_title"] = Path(path).name
    doc.metadata["parent_id"] = parent_id
    doc.metadata["chunk_id"] = str(uuid.uuid4()) 

  document_ids = vector_store.add_documents(docs)


def group_by_parents(child_hits: List[Document]) -> dict:
  output = {} 
  for child in child_hits:
    parent_id = child.metadata.get("parent_id")
    if output.get(parent_id) is None:
      output[parent_id] = [child]
    else:
      output.get(parent_id).append(child)
  return output

class State(AgentState):
  citations: Any

class RetrieveDocumentsMiddleware(AgentMiddleware[State]):
    state_schema = State
    
    @traceable
    def before_model(self, state: AgentState) -> dict[str, Any] | None:
      last_message = state["messages"][-1]
      retrieved = vector_store.similarity_search_with_score(last_message.text, k=5)
      parents: dict[str, List[Tuple[Document, float]]] = {}
      for chunk, dist in retrieved:
        pid = chunk.metadata.get("parent_id")
        parents.setdefault(pid, []).append((chunk, dist))
      
      scored: List[Tuple[str, float, Document]] = []
      for pid, hits in parents.items():
        min_dist = min(dist for _, dist in hits)
        scored.append((pid, min_dist, hits))

      scored.sort(key=lambda x: x[1])
      
      best = scored[0][1]
      delta = 0.05
      max_parents = 2

      chosen = [(pid, score, hits) for pid, score, hits in scored 
                if score <= best + delta][:max_parents]

      parent_ids = [pid for pid, _, _ in chosen]
      print(f"PARENT IDS: \n{parent_ids}")
      parent_records_content = [parentDB.get(id).get("content") for id in parent_ids]
      docs_content = "\n\n".join(content for content in parent_records_content)

      print(f"PULLED:\n")
      for d, s in retrieved:
        print(f"\nScore: {s} - Document: {d.metadata.get("doc_title")}")
      
      print(f"Filtered completed:\n:")
      for pid, score, hits in chosen:
        print(f"\nScore: {score}")
      
      augmented_message_content = (
        f"{last_message.text}\n\n"
        "You are a helpful assistant trying to help me understand my companies internal documents. \n"
        "Use the ONLY following context in your response. If you do not know, say you don't know. No guessing allowed.\n\n"
        f"CONTEXT:\n{docs_content}"
      )
      citations = []
      for pid, score, hits in chosen:
        rec = parentDB[pid]
        chunks = []
        for h, _ in hits:
          chunks.append({
            "chunk_id": h.metadata["chunk_id"],
            "section": h.metadata["section"],
            "title": h.metadata["title"]
          })
        citations.append({
            "doc_title": rec["doc_title"],
            "source_path": rec["source_path"],
            "parent_id": pid,
            "chunks": chunks
        })

      return {
          "messages": [last_message.model_copy(update={"content": augmented_message_content})],
          "citations": citations


      }


agent = create_agent(model, tools=[], middleware=[RetrieveDocumentsMiddleware()])

def query_assistant(query: str) -> dict:
  response = agent.invoke({
    "messages": [{"role": "user", "content": query}],
  })

  answer = response["messages"][-1].content
  citations = response["citations"]
  
  return {
    "content": answer,
    "citations": citations
  }


