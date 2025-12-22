import type { ServerMessage, WSHandlers } from '../types'

const WS_URL = "ws://127.0.0.1:8000/ws"

export const createWebSocket = (handlers: WSHandlers) => {
  const ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    console.log("WS connected");
    handlers.onOpen();
  };

  ws.onerror = (err) => {
    console.error("WS error:", err);
  };
  
  ws.onclose = () => {
    console.log("WS disconnected");
    handlers.onClose()
  };

  ws.onmessage = (event: MessageEvent) => {
    const response = JSON.parse(event.data) as ServerMessage
    handlers.onMessage(response);
  };

  const close = () => {
    ws.close();
  }

  const sendMessage = (message: string) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(message);
    }
  };

  const isReady = () => {
    return ws && ws.readyState === WebSocket.OPEN ? true : false;
  }
  
  return {
    close,
    sendMessage,
    isReady
  };
};






