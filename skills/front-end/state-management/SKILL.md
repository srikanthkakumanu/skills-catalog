---
name: state-management
description: >
  Use when deciding where a piece of state should live in a React/Next.js app — component state,
  URL state, or server state — or when diagnosing unnecessary re-renders from state placement.
  Covers useState/useReducer/context for UI state, useSearchParams for shareable filter/sort/
  pagination state, and why server data should not be forked into a second local copy.
---

# State Management

Three kinds of state show up in almost every screen, and each has a correct home. Picking the
wrong one is the most common source of both bugs (state that should persist doesn't) and
performance problems (state that shouldn't trigger a re-render does).

## The Three Kinds of State

| Kind | Home | Examples |
|---|---|---|
| Server state | TanStack Query (see `data-fetching`) | Fetched records, anything that can go stale |
| URL state | `useSearchParams` / route params | Filters, sort order, pagination, selected tab — anything that should survive a refresh or be shareable via link |
| UI state | `useState` / `useReducer` / local context | Modal open/closed, form draft (unless RHF-managed), hover/focus state |

## URL State for Shareable, Refresh-Safe UI

Filter, sort, and pagination state that a user would expect to survive a page refresh or be
shareable via a copied link belongs in the URL, not in `useState`.

```tsx
// Bad — filters vanish on refresh, can't be shared as a link, back button does nothing useful
function ProductList() {
  const [status, setStatus] = useState('active');
  const [page, setPage] = useState(1);
  // ...
}

// Good — filters are the URL; refresh, share, and back/forward all work correctly
'use client';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';

function ProductList() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const status = searchParams.get('status') ?? 'active';
  const page = Number(searchParams.get('page') ?? '1');

  function setStatus(next: string) {
    const params = new URLSearchParams(searchParams);
    params.set('status', next);
    params.set('page', '1');
    router.push(`${pathname}?${params.toString()}`);
  }
  // ...
}
```

## Don't Fork Server Data Into useState

A `useQuery`/`useSuspenseQuery` result already lives in TanStack Query's cache. Copying it into a
`useState` on mount creates a second, unsynchronized copy that silently drifts from the cache after
the next refetch or mutation.

```tsx
// Bad — forks server data into local state; a refetch updates the cache but not this copy
function OrderSummary({ orderId }: { orderId: string }) {
  const { data } = useQuery({ queryKey: ['order', orderId], queryFn: () => fetchOrder(orderId) });
  const [order, setOrder] = useState(data);
  // `order` never updates again after the initial render
  return <div>{order?.total}</div>;
}

// Good — read straight from the query result; it's already reactive
function OrderSummary({ orderId }: { orderId: string }) {
  const { data: order } = useQuery({ queryKey: ['order', orderId], queryFn: () => fetchOrder(orderId) });
  return <div>{order?.total}</div>;
}
```

## Split Contexts by Concern

A single context holding unrelated pieces of state re-renders every consumer whenever any piece
changes, even the ones that only read an unrelated field. Split by what actually changes together.

```tsx
// Bad — a Theme change re-renders every consumer of AuthContext too
const AppContext = createContext<{ theme: Theme; user: User | null }>(/* ... */);

// Good — independent contexts, independent re-render scopes
const ThemeContext = createContext<Theme>('light');
const AuthContext = createContext<User | null>(null);
```

## Derive, Don't Duplicate

If a value can be computed from existing state or props during render, compute it — don't store a
derived value in its own `useState` and try to keep it in sync with an effect.

```tsx
// Bad — a second state variable that must be kept in sync with items via an effect
const [items, setItems] = useState<Item[]>([]);
const [total, setTotal] = useState(0);
useEffect(() => setTotal(items.reduce((s, i) => s + i.price, 0)), [items]);

// Good — derived during render, always correct, no effect needed
const [items, setItems] = useState<Item[]>([]);
const total = items.reduce((s, i) => s + i.price, 0);
```

## Official sources

- React state docs: https://react.dev/learn/managing-state
- Next.js `useSearchParams`: https://nextjs.org/docs/app/api-reference/functions/use-search-params
- Adapted from Vercel's `react-best-practices` re-render optimization rule category
  (`rerender-derived-state`, `rerender-derived-state-no-effect`, `rerender-split-combined-hooks`):
  https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent stores filter/sort/pagination in `useState` — put it in the URL via `useSearchParams` so refresh and sharing work.
- Agent copies a TanStack Query result into `useState` on mount — read the query result directly; it's already reactive.
- Agent derives a value with `useState` + a syncing `useEffect` — compute it inline during render instead.
- Agent puts unrelated state fields in one context — split into separate contexts by what changes together.
- Agent lifts state higher than its nearest common consumer needs — widens the re-render blast radius for no benefit.
