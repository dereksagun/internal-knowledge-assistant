function Home({ onStart }: { onStart: () => void }) {
  return (
    <div className="h-full flex flex-col">
      {/* Top bar */}
      <div className="border-b border-zinc-800 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto max-w-5xl px-5 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-2xl border border-zinc-800 bg-zinc-900/50 grid place-items-center">
              <span className="text-sm font-semibold">IK</span>
            </div>
            <div>
              <div className="text-sm font-semibold">Internal Knowledge Assistant</div>
              <div className="text-xs text-zinc-400">RAG-powered Assistant</div>
            </div>
          </div>
          <button
            onClick={onStart}
            className="rounded-2xl bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 hover:opacity-90"
          >
            Open Chat
          </button>
        </div>
      </div>

      {/* Hero */}
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-5xl px-5 py-10">
          <div className="grid gap-8 lg:grid-cols-1 lg:items-center">
            <div>
              <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">
                Ask your internal docs.
                <span className="block text-zinc-400">Get answers with sources.</span>
              </h1>
              <p className="mt-4 text-zinc-300 leading-relaxed">
                This is a demo of an <span className="font-medium">Internal Knowledge Assistant</span> designed to let employees chat directly with a company’s internal documents. 
                Instead of tediously searching through handbooks, wikis, or policy pages, users can ask natural-language questions and receive clear, 
                grounded answers. The system is <span className="font-medium">RAG-powered</span>, uses a <span className="font-medium">custom chunking strategy</span>, and returns <span className="font-medium">deterministic citations</span> so every answer 
                can be traced back to its source.
              </p>

              <div className="mt-6 flex flex-col sm:flex-row gap-1">
                <button
                  onClick={onStart}
                  className="rounded-2xl bg-zinc-100 px-5 py-3 text-sm font-medium text-zinc-450 hover:opacity-90"
                >
                  Start a chat
                </button>
              </div>

            </div>

            
          </div>
          <div className="mt-6 flex flex-wrap gap-2">
                <Badge>Retrieval-Augmented Generation(RAG)</Badge>
                <Badge>ChromaDb</Badge>
                <Badge>Open AI</Badge>
                <Badge>Langchain</Badge>
                <Badge>Websockets</Badge>
              </div>
          {/* How it works */}
          <div id="how-it-works" className="mt-12 grid gap-4 md:grid-cols-3">
            <InfoCard
              title="1) Retrieve"
              body="We embed and index document chunks. For each question, we retrieve the top-k relevant chunks."
            />
            <InfoCard
              title="2) Generate"
              body="We send only the retrieved context to the model with strict instructions to avoid guessing."
            />
            <InfoCard
              title="3) Return sources"
              body="We return deterministic sources from chunk metadata (title/section/path/chunk_id), ready for a JSON API."
            />
          </div>

          <div className="mt-10 rounded-3xl border border-zinc-800 bg-zinc-900/30 p-5">
            <div className="text-sm font-semibold">What you can demo</div>
            <ul className="mt-3 space-y-2 text-sm text-zinc-300 list-disc pl-5">
              <li>Ask policy / onboarding / product questions and get grounded answers.</li>
              <li>Show sources under each answer (doc title + section).</li>
              <li>Prove determinism: same query returns the same source set (given same index).</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-zinc-800 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto max-w-5xl px-5 py-4 text-xs text-zinc-500 flex items-center justify-between">
          <span>Built for demoing RAG + citations</span>
          <button onClick={onStart} className="text-zinc-300 hover:text-zinc-100">
            Open chat →
          </button>
        </div>
      </div>
    </div>
  );
}


function InfoCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-900/30 p-5">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-2 text-sm text-zinc-300 leading-relaxed">{body}</div>
    </div>
  );
}

function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full border border-zinc-800 bg-zinc-900/40 px-3 py-1 text-xs text-zinc-300">
      {children}
    </span>
  );
}


export default Home