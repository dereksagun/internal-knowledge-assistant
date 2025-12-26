from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from src.core.container import get_deps
from src.services.agent_service import build_agent_service
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
deps = get_deps()
handle_message = build_agent_service(deps)

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  try:
    while True:
      data = await websocket.receive_text()
      output = await handle_message(data)
      await websocket.send_text(json.dumps(output))
  except WebSocketDisconnect:
    print("WebSocket disconnected")
    