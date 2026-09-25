---
name: nextjs-app-router
description: >
  Use when building Next.js 16 applications with the App Router — routing, layouts, Server and
  Client Components, data fetching cache intent, streaming with Suspense, Server Actions,
  route-segment loading/error boundaries, or SEO metadata. Triggers on: Next.js, App Router, RSC,
  use server, use client, Server Components, Server Actions, generateMetadata, loading.tsx,
  error.tsx, Next.js deployment, Turbopack.
---

# Next.js 16 App Router

Next.js 16 uses the `app/` directory exclusively — never the legacy `pages/` router. Turbopack is
the default dev and build bundler.

## Server Components by Default

Every component under `app/` is a Server Component unless it opts into `'use client'`. Push
`'use client'` to the smallest leaf that actually needs interactivity (event handlers, state,
browser APIs) — never mark a whole page or layout as client just because one child needs it.

```tsx
// Bad — the whole page becomes a Client Component for one button's onClick
'use client';

export default function ProductPage({ product }: { product: Product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <button onClick={() => addToCart(product.id)}>Add to cart</button>
    </div>
  );
}

// Good — the page stays a Server Component; only the interactive leaf opts in
export default function ProductPage({ product }: { product: Product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  );
}
```

## Explicit Cache Intent on Every fetch

Never call `fetch` with implicit caching behavior. State the intent — cache indefinitely, revalidate
on an interval, or opt out — every time.

```tsx
// Bad — cache behavior is whatever the default happens to be; not stated, not reviewable
const res = await fetch('https://api.example.com/products');

// Good — explicit revalidation window (ISR)
const res = await fetch('https://api.example.com/products', { next: { revalidate: 60 } });

// Good — explicitly always-fresh
const res = await fetch('https://api.example.com/cart', { cache: 'no-store' });
```

## Streaming with Suspense and loading.tsx

Every route segment that performs async data fetching gets a `loading.tsx` (route-level streaming
fallback) and an `error.tsx` (segment-level error boundary). Use `<Suspense>` inside a page to
stream in slower sub-sections without blocking the whole page.

```tsx
// app/products/[id]/page.tsx
import { Suspense } from 'react';

export default function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <ProductHeader id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <ProductReviews id={params.id} />
      </Suspense>
    </div>
  );
}
```

A ready-to-copy four-file route-segment bundle (`page.tsx`, `loading.tsx`, `error.tsx`,
`layout.tsx`) is in `templates/route-segment/`.

## Server Actions for Mutations

Use a Server Action (`'use server'`) for form submissions and mutations instead of a hand-rolled
API route when the caller is a form in the same app.

```tsx
// app/products/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createProduct(formData: FormData) {
  const name = formData.get('name') as string;
  await db.product.create({ data: { name } });
  revalidatePath('/products');
}
```

Reserve Route Handlers (`app/api/*/route.ts`) for endpoints an external client or webhook calls —
not for form submissions from this app's own UI.

## generateMetadata for SEO

Never hand-write `<title>`/`<meta>` tags in JSX. Use the static `metadata` export or
`generateMetadata` for dynamic per-page SEO.

```tsx
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const product = await fetchProduct(params.id);
  return {
    title: product.name,
    description: product.description,
    openGraph: { title: product.name, images: [product.imageUrl] },
  };
}
```

## next/image and next/font Always

Never use a raw `<img>` tag for content images or a `<link>` font tag — both bypass Next.js's
optimization pipeline (responsive sizing, lazy loading, layout-shift prevention, self-hosted fonts).

## Official sources

- App Router: https://nextjs.org/docs/app
- Server and Client Components: https://nextjs.org/docs/app/building-your-application/rendering/server-components
- Data fetching and caching: https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating
- Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- Adapted from jeffallan's `nextjs-developer` skill (MUST DO/MUST NOT DO constraints) and Vercel's
  `react-best-practices` `server-*` rule category: https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent marks a whole page/layout `'use client'` for one interactive child — push `'use client'` to the leaf only.
- Agent calls `fetch` with no cache option — always state `next: { revalidate }` or `cache: 'no-store'` explicitly.
- Agent skips `loading.tsx`/`error.tsx` on an async route segment — add both, or a slow/failing fetch has no boundary.
- Agent hand-writes `<title>`/`<meta>` in JSX — use `generateMetadata` or the static `metadata` export.
- Agent uses a plain `<img>` for a content image — use `next/image`.
- Agent builds a Route Handler for a same-app form submission — use a Server Action instead.
- Agent converts a component to Client just to read server-fetched data — fetch server-side and pass it down as props instead.
- Agent deploys without running `next build` locally first — confirm zero type errors and check `NEXT_PUBLIC_*` vs server-only env vars before shipping.
