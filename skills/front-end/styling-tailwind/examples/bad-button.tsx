// BAD - inline giant class string (unmaintainable, drifts per call site), hardcoded color, unconditional animation.
export function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="inline-flex animate-bounce items-center rounded-md bg-[#3b82f6] px-4 py-2 text-white hover:bg-[#2563eb] disabled:opacity-50">
      {children}
    </button>
  );
}
