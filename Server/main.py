from src.agent.agent import query_assistant
from fastapi import FastAPI, WebSocket
import json


app = FastAPI()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    print(f"recieved: \n{data}" )
    query_assistant(data)
    output = query_assistant(data)
    await websocket.send_text(json.dumps(output))
    