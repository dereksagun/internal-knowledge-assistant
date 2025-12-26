import json
from pydantic import BaseModel
from src.core.agent import create_new_agent
from src.core.container import Deps
class RagResponse(BaseModel):
     answer: str
     answer_found: bool
     
def build_agent_service(deps: Deps):
  agent = create_new_agent(deps)
  
  async def handle_user_message(query: str) -> dict:
    response = agent.invoke({
      "messages": [{"role": "user", "content": query}],
    })
    print(response["messages"][-1].content)
    content = json.loads(response["messages"][-1].content)
    print(content)

    answer_found = content["answer_found"]

    answer = content["answer"]
    if answer_found:
      citations = response["citations"] 
    else:
      citations = []
    
    return {
      "content": answer,
      "citations": citations
    }
  
  return handle_user_message
