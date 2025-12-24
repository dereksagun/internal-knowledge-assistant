from src.core.agent import create_new_agent

def build_agent_service(deps):
  agent = create_new_agent(deps)

  async def handle_user_message(query: str) -> dict:
    response = agent.invoke({
      "messages": [{"role": "user", "content": query}],
    })

    answer = response["messages"][-1].content
    citations = response["citations"]
    
    return {
      "content": answer,
      "citations": citations
    }
  
  return handle_user_message
