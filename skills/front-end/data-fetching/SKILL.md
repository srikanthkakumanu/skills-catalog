---
name: data-fetching
description: >
  Use when fetching, caching, or mutating server data on the client with TanStack Query — query key
  design, staleTime/gcTime tuning, mutations and cache invalidation, optimistic updates,
  useSuspenseQuery with Suspense, parallel fetching to avoid waterfalls, or server-side
  prefetch/hydrate for Server Components. For choosing whether data belongs in TanStack Query at
  all vs URL/UI state, see state-management.
---

# Data Fetching (TanStack Query)

TanStack Query (`@tanstack/react-query`) owns all client-side server state — anything fetched from
an API and cacheable. It replaces hand-rolled `useEffect` + `useState` fetch logic.

## Provider Setup

A `QueryClientProvider` boundary is required once, inside a Client Component wrapper — the
`QueryClient` itself must not be created at module scope shared across requests on the server (that
leaks cache between users). A ready-to-copy provider is in `templates/queryClient.tsx`.

## Query Keys Must Include Every Input

A query key is the cache key. Every value the query function's result depends on must be in the
key, or a component reading with different filter/id values will silently see stale/wrong cached
data instead of refetching.

```tsx
// Bad — key doesn't include status; switching status filters returns the wrong cached page
useQuery({ queryKey: ['orders'], queryFn: () => fetchOrders(status) });

// Good — key includes every input the query depends on
useQuery({ queryKey: ['orders', { status }], queryFn: () => fetchOrders(status) });
```

## Basic Query with Loading/Error States

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 60_000, // treat as fresh for 60s — no refetch on remount within that window
  });

  if (isPending) return <ProfileSkeleton />;
  if (isError) return <ErrorMessage message={error.message} />;
  return <ProfileCard user={data} />;
}
```

## Mutations and Cache Invalidation

```tsx
function useUpdateOrder() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: UpdateOrderInput) => updateOrder(input),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['order', variables.orderId] });
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
}
```

## Optimistic Updates

```tsx
useMutation({
  mutationFn: toggleFavorite,
  onMutate: async (productId) => {
    await queryClient.cancelQueries({ queryKey: ['favorites'] });
    const previous = queryClient.getQueryData<string[]>(['favorites']);
    queryClient.setQueryData<string[]>(['favorites'], (old = []) =>
      old.includes(productId) ? old.filter((id) => id !== productId) : [...old, productId]
    );
    return { previous };
  },
  onError: (_err, _productId, context) => {
    if (context?.previous) queryClient.setQueryData(['favorites'], context.previous);
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['favorites'] }),
});
```

## Parallel Fetching, Not Waterfalls

Independent queries should fire together, not one-after-another via sequential `await`s or nested
components each blocking on their own fetch.

```tsx
// Bad — three sequential round trips
const user = await fetchUser(id);
const orders = await fetchOrders(id);
const reviews = await fetchReviews(id);

// Good — one round trip's worth of latency
const [user, orders, reviews] = await Promise.all([fetchUser(id), fetchOrders(id), fetchReviews(id)]);

// Good — client-side equivalent with useQueries for independent parallel queries
const results = useQueries({
  queries: [id1, id2, id3].map((id) => ({ queryKey: ['user', id], queryFn: () => fetchUser(id) })),
});
```

## Server-Side Prefetch + Hydrate (App Router)

Prefetch in a Server Component and hydrate into the client cache so the first client render already
has data — avoids a client-side loading spinner for data the server already had.

```tsx
// Server Component
async function ProductPage({ params }: { params: { id: string } }) {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery({
    queryKey: ['product', params.id],
    queryFn: () => fetchProduct(params.id),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <ProductDetails id={params.id} />
    </HydrationBoundary>
  );
}
```

## Official sources

- TanStack Query docs: https://tanstack.com/query/latest/docs/framework/react/overview
- Query keys: https://tanstack.com/query/latest/docs/framework/react/guides/query-keys
- SSR with Next.js App Router: https://tanstack.com/query/latest/docs/framework/react/guides/ssr
- Adapted from Vercel's `react-best-practices` `async-*`/`server-*` rule categories
  (`async-parallel`, `server-cache-react`, `server-parallel-fetching`):
  https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent writes `useEffect` + `useState` for a data fetch — use `useQuery` instead; it handles caching, loading, error, and refetch.
- Agent omits a filter/id from the query key — the cache returns stale data for a different filter value; include every input.
- Agent creates a single module-level `QueryClient` shared across server requests — create one per request/render on the server.
- Agent chains sequential `await`s for independent data — use `Promise.all` or parallel `useQueries`.
- Agent skips `onError` rollback on an optimistic update — a failed mutation leaves the UI showing the wrong state.
- Agent forgets to invalidate related queries after a mutation — stale cached data lingers after a successful write.
- Agent forks a query result into local `useState` — see `state-management`'s "Don't fork server data" gotcha.
