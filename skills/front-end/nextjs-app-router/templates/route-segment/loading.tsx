// Streaming fallback shown while page.tsx's async work resolves.
export default function Loading() {
  return <div aria-busy="true">Loading…</div>;
}
