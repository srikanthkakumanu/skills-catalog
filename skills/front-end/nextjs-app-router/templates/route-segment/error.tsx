// Segment-level error boundary. Must be a Client Component — Next.js requires this.
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div role="alert">
      <p>Something went wrong loading this page.</p>
      <button type="button" onClick={() => reset()}>
        Try again
      </button>
    </div>
  );
}
