from typing import Any, List
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


from langchain_core.documents import Document

def find_all_files_paths(path: Path, list_of_paths: List[str]):
  """Retrieves the paths of all the files in the starting directory"""
  for child in path.iterdir():
    if child.is_file():
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
  embedding_function=embeddings
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
find_all_files_paths(Path.cwd() / 'docs', paths)

for path in paths:
  loader = Docx2txtLoader(path)
  document_files = loader.load()
  docs = markdown_splitter.split_text(document_files[0].page_content)
  for doc in docs:
    doc.metadata["source_path"] = path
    doc.metadata["last_updated"] = date.today().strftime("%Y-%m-%d")
    doc.metadata["doc_title"] = Path(path).name
  
  document_ids = vector_store.add_documents(docs)

class State(AgentState):
  documents: list[Document]

class RetrieveDocumentsMiddleware(AgentMiddleware[State]):
    state_schema = State
    
    @traceable
    def before_model(self, state: AgentState) -> dict[str, Any] | None:
      last_message = state["messages"][-1]
      retrieved = vector_store.similarity_search_with_score(last_message.text, k=5)
      #print(f"SCORE: \n\n\n\n\n\n {retrieved[0][1]}")
      filtered_docs = [d for d, s in retrieved if s <= .75]
      for d, s in retrieved:
        print(f"\nScore: {s} - Document: {d.metadata.get("doc_title")}")
      
      docs_content = "\n\n".join(doc.page_content for doc in filtered_docs)

      augmented_message_content = (
        f"{last_message.text}\n\n"
        "You are a helpful assistant trying to help me understand my companies internal documents. \n"
        "Use the ONLY following context in your response. If you do not know, say you don't know. No guessing allowed.\n\n"
        f"CONTEXT:\n{docs_content}"
      )

      return {
          "messages": [last_message.model_copy(update={"content": augmented_message_content})],
          "documents": filtered_docs,
      }


agent = create_agent(model, tools=[], middleware=[RetrieveDocumentsMiddleware()])

'''
while True:
  query = input("What is your question?\n")
  response = agent.invoke({
    "messages": [{"role": "user", "content": query}],
  })

  answer = response["messages"][-1].content
  docs = response["documents"]
  citations = []
  for doc in docs:
    citation = {
        "doc_title": doc.metadata.get("doc_title"),
        "title": doc.metadata.get("title"),
        "last_updated": doc.metadata.get("last_updated"),
        "section": doc.metadata.get("section")
        
    }
    citation = {k: v for k, v in citation.items() if v is not None}
    citations.append(citation)

  output = {
    "answer": answer,
    "citations": citations
  }
  pprint.pprint(output)
'''

def query_assistant(query: str) -> dict:
  response = agent.invoke({
    "messages": [{"role": "user", "content": query}],
  })

  answer = response["messages"][-1].content
  docs = response["documents"]
  citations = []
  for doc in docs:
    citation = {
        "doc_title": doc.metadata.get("doc_title"),
        "title": doc.metadata.get("title"),
        "last_updated": doc.metadata.get("last_updated"),
        "section": doc.metadata.get("section"),
        "source_path": doc.metadata.get("source_path")
        
    }
    citation = {k: v for k, v in citation.items() if v is not None}
    citations.append(citation)
  
  return {
    "answer": answer,
    "citations": citations
  }




'''
[
  Document(
    id='9a2ab187-8991-42a1-9f01-413496ea16c7', 
    metadata={
      'title': 'Paid Time Off (PTO) Policy', 
      'doc_title': 'pto_policy.docx', 
      'section': 'Approval', 
      'last_updated': '2025-12-19', 
      'source_path': '/Users/dereksagun/Documents/Code/pythonstuff/AI/Chatbot/Server/docs/handbook/pto_policy.docx'
    }, 
    page_content='PTO must be approved by a manager at least 2 weeks in advance.'
  ), 
  Document(
    id='feec4909-e556-4278-8b17-a6b3fc508169', 
    metadata={
      'title': 'Paid Time Off (PTO) Policy', 
      'last_updated': '2025-12-19', 
      'doc_title': 'pto_policy.docx', 
      'source_path': '/Users/dereksagun/Documents/Code/pythonstuff/AI/Chatbot/Server/docs/handbook/pto_policy.docx', 
      'section': 'Policy'
    }, 
    page_content='Prox Labs offers 20 days of PTO per year.'
  ), 
  Document(
    id='8dd5d693-cb74-47da-a833-08c191229d7a', 
    metadata={
      'last_updated': '2025-12-19', 
      'source_path': '/Users/dereksagun/Documents/Code/pythonstuff/AI/Chatbot/Server/docs/handbook/pto_policy.docx', 
      'doc_title': 'pto_policy.docx', 
      'section': 'Rollover', 
      'title': 'Paid Time Off (PTO) Policy'
    }, 
    page_content='Up to 5 unused PTO days may roll over into the next calendar year.'
  ), 
  Document(
    id='0989c0e9-30a9-4351-b663-e05ba75320da', 
    metadata={
      'source_path': '/Users/dereksagun/Documents/Code/pythonstuff/AI/Chatbot/Server/docs/traps/misleading_doc.docx', 
      'last_updated': '2025-12-19', 
      'doc_title': 'misleading_doc.docx', 
      'title': 'PTO Clarifications (Draft)'
    }, 
    page_content='Last Updated: 2022-01-01  \nThis document discusses industry PTO trends.  \nIt does NOT reflect Prox Labs policy.'
  )
]

'''
  

