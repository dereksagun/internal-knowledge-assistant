from typing import Any
from langsmith import traceable
from langchain.agents.middleware import AgentState, AgentMiddleware
from src.utils.reranker import find_parent_docs, get_parent_ids, find_best_parent_scores
from src.utils.citations import build_citations
from langchain.agents import create_agent
from src.core.container import Deps

def create_new_agent(deps: Deps):
  class State(AgentState):
    citations: Any

  class RetrieveDocumentsMiddleware(AgentMiddleware[State]):
      state_schema = State
      
      @traceable
      def before_model(self, state: AgentState) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        retrieved = deps.vector_store.similarity_search_with_score(last_message.text, k=5)
        
        parents = find_parent_docs(retrieved)
        chosen = find_best_parent_scores(parents)
        parent_ids = get_parent_ids(chosen)
        
        parent_chunks = [deps.parent_db.get_content(pid) for pid in parent_ids]
        docs_content = "\n\n".join(parent_chunks)

        augmented_message_content = (
          f"{last_message.text}\n\n"
          "You are a helpful assistant trying to help me understand my companies internal documents. \n"
          "Use the ONLY following context in your response. If you do not know, say you don't know. No guessing allowed.\n\n"
          f"CONTEXT:\n{docs_content}"
        )
        citations = build_citations(chosen, deps)
      
        return {
            "messages": [last_message.model_copy(update={"content": augmented_message_content})],
            "citations": citations

        }
  agent = create_agent(deps.llm, tools=[], middleware=[RetrieveDocumentsMiddleware()])
  return agent
      

'''
def group_by_parents(child_hits: List[Document]) -> dict:
  output = {} 
  for child in child_hits:
    parent_id = child.metadata.get("parent_id")
    if output.get(parent_id) is None:
      output[parent_id] = [child]
    else:
      output.get(parent_id).append(child)
  return output

print(f"PULLED:\n")
for d, s in retrieved:
  print(f"\nScore: {s} - Document: {d.metadata.get("doc_title")}")

print(f"Filtered completed:\n:")
for pid, score, hits in chosen:
  print(f"\nScore: {score}")
'''
