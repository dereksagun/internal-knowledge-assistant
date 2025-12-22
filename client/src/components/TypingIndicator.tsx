export const TypingIndicator = () => {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/60 px-4 py-2">
      <div className="flex items-center gap-1">
        <Dot delayClass="animate-[bounce_1s_infinite]" />
        <Dot delayClass="animate-[bounce_1s_0.15s_infinite]" />
        <Dot delayClass="animate-[bounce_1s_0.3s_infinite]" />
      </div>
    </div>
  );
}

const Dot = ({ delayClass }: { delayClass: string }) => {
  return (
    <span
      className={[
        "inline-block h-2 w-2 rounded-full bg-zinc-300/80",
        delayClass,
      ].join(" ")}
    />
  );
}

