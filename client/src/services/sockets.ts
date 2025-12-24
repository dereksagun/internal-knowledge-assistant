import type { ServerMessage, WSHandlers } from '../types'


export const createWebSocket = (handlers: WSHandlers) => {
  const ws = new WebSocket(import.meta.env.VITE_WS_URL);

  ws.onopen = () => {
    console.log("WS connected");
    handlers.onOpen();
  };

  ws.onerror = () => {
  };
  
  ws.onclose = () => {
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






