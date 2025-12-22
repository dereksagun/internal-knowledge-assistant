import { useEffect, useMemo, useRef, useState } from 'react';
import {createWebSocket} from '../services/sockets';
import type { ChatMessage, ServerMessage } from '../types';
import MessageBubble from '../components/MessageBubble';
import { TypingIndicator } from '../components/TypingIndicator';

const uid = () => Math.random().toString(36).slice(2) + Date.now().toString(36);
const getCurrentDateTime = () => Date.now();

const Chat = ({onBack} : {onBack: () => void}) => {
  const wsRef = useRef<ReturnType<typeof createWebSocket> | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const [isConnected, setIsConnected] = useState(false);
  const [input, setInput] = useState<string>('')
  const [isSending, setIsSending] = useState<boolean>(false);
  const [chat, setChat] = useState<ChatMessage[]>([
    {
      id: uid(),
      role: "assistant",
      content: "Ask me anything about the internal docs.",
      createdAt: getCurrentDateTime(),
    },
  ]);
  
  useEffect(() => {
    wsRef.current = createWebSocket({
      onOpen: () => setIsConnected(true),
      onClose: () => setIsConnected(false),
      onError: () => setIsConnected(false),
      onMessage: (response: ServerMessage) => {
        setChat(prev => [...prev, {
          id: uid(),
          role: "assistant",
          content: response.content,
          citations: response.citations ?? [],
          createdAt: Date.now(),
        }])
        setIsSending(false);
      }
    });

    return () => {
      wsRef.current?.close();
    };

  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({behavior: "smooth"});
  }, [chat.length])

  const canSend = useMemo(() => {
    return isConnected && input.trim().length > 0 && !isSending;
  }, [isConnected, input, isSending]);
  
  const send = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if(!input || !wsRef.current?.isReady()) return;
    setChat((prev) => [
      ...prev,
      { id: uid(), role: "user", content: input, createdAt: getCurrentDateTime() }
    ]);

    setInput("");
    setIsSending(true);
    wsRef.current.sendMessage(input);
  };

  return (
    <div className="mx-auto h-screen flex flex-col bg-zinc-950 text-zinc-100">
      {/* Header */}
      <div className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-3">
        <button
              onClick={onBack}
              className="rounded-xl border border-zinc-800 px-3 py-1.5 text-xs text-zinc-300 hover:bg-zinc-900"
            >
              ← Home
            </button>
        <div>
            <div className="text-sm font-semibold">Internal Knowledge Assistant</div>
            <div className="text-xs text-zinc-400">
              Status:{" "}
              <span className={isConnected ? "text-emerald-400" : "text-rose-400"}>
                {isConnected ? "Connected" : "Disconnected"}
              </span>
              {isSending ? <span className="ml-2 text-zinc-500">• Thinking…</span> : null}
            </div>
          </div>
          <button
            onClick={() => setChat((prev) => prev.slice(0, 1))}
            className="rounded-xl border border-zinc-800 px-3 py-1.5 text-xs text-zinc-300 hover:bg-zinc-900"
          >
            Clear
          </button>
        </div>
      </div>
      {/* Chat */}
      <div className="w-full flex-1 overflow-y-auto">
        <div className="w-full mx-auto flex max-w-3xl flex-col gap-4 px-4 py-6">
          {chat.map((m) => (
            <MessageBubble key={m.id} msg={m} />
          ))}

          {isSending ? (
            <div className="flex justify-center py-2">
                <TypingIndicator />
            </div>
          ) : null}
          <div ref={bottomRef} />
        </div>
      </div>
      {/* Input */}
      <div className="border-t border-zinc-800 bg-zinc-950/80 backdrop-blur">
        <form onSubmit={send} className="mx-auto flex max-w-3xl gap-2 px-4 py-3">
          <div className="flex-1 rounded-2xl border border-zinc-800 bg-zinc-900/40 px-3 py-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question…"
              className="w-full bg-transparent text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={!canSend}
            className="rounded-2xl bg-zinc-100 px-4 py-2 text-sm font-medium text-sm text-zinc-400 disabled:opacity-40"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default Chat
