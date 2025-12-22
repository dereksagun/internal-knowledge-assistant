import type { ChatMessage } from "../types";

const MessageBubble = ({ msg }: { msg: ChatMessage }) => {
  const isUser = msg.role === "user";

  return (
    <div className={"flex " + (isUser ? "justify-end" : "justify-start")}>
      <div
        className={[
          "max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-zinc-100 text-zinc-950"
            : "bg-zinc-900/60 text-zinc-100 border border-zinc-800",
        ].join(" ")}
      >
        <div className="whitespace-pre-wrap">{msg.content}</div>

        {"citations" in msg && msg.citations && msg.citations.length > 0 ? (
          <div className="mt-3 border-t border-zinc-800 pt-2">
            <div className="text-[11px] font-semibold text-zinc-400">Sources</div>
            <ul className="mt-1 space-y-1">
              {msg.citations.slice(0, 5).map((c, idx) => (
                <li key={idx} className="text-[11px] text-zinc-400">
                  {c.doc_title ?? "Unknown doc"}
                  {c.chunks.map((chunk,idx) => (
                    <li key={idx} className="text-[11px] text-zinc-400">
                      {chunk.section ? <span className="text-zinc-500">• {chunk.title + " > "} {chunk.section}</span> : null}
                      </li>
                  ))}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default MessageBubble