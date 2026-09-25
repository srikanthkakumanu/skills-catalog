---
name: nextjs-project-conventions
description: >
  House project conventions for Next.js 16 / React 19 / TypeScript 5.9 frontend projects on pnpm —
  App Router folder structure, Server/Client Component boundary rules, environment variable
  handling, and git conventions. Loaded unconditionally for every frontend context by
  implementation-guide, never resolved per-topic.
---
# Next.js and Frontend Project Instructions

Next.js 16 App Router, React 19, TypeScript 5.9 (strict). pnpm package manager.

## Workflow

- **Implement** — Server Components by default; see `skills/frontend/nextjs-app-router` and
  `skills/frontend/react-component-patterns`
- **Fetch data** — TanStack Query on the client, `fetch`/direct calls in Server Components; see
  `skills/frontend/data-fetching`
- **Test** — write unit/component + e2e tests (see `## Testing` below), run `pnpm test` and
  `pnpm test:e2e`, confirm all pass
- **Deploy** — run `pnpm build` and confirm zero type errors before shipping

## Commands

- `pnpm dev` — start the dev server (Turbopack)
- `pnpm build` — production build
- `pnpm test` — run Vitest unit/component tests
- `pnpm test:e2e` — run Playwright end-to-end tests
- `pnpm lint` — ESLint
- `pnpm typecheck` — `tsc --noEmit`

Run `pnpm typecheck && pnpm lint && pnpm test` before committing.

## Architecture

Standard App Router structure:

- `app/` — routes; each segment gets `page.tsx`, and `loading.tsx`/`error.tsx` where it fetches data
  - `app/api/` — Route Handlers, only for endpoints an external client/webhook calls
- `components/` — shared, reusable components (not route-specific)
- `lib/` — non-component code: API clients, utilities, Zod schemas
- `hooks/` — shared custom hooks
- Route-specific components/tests are colocated inside their route segment, not in `components/`

## Coding Conventions

- TypeScript 5.9 strict mode (this catalog's only supported version — see
  `../typescript-language-conventions/SKILL.md`)
- Server Components by default; `'use client'` only at the smallest interactive leaf — see
  `skills/frontend/nextjs-app-router`
- Environment variables: `NEXT_PUBLIC_*` prefix only for values safe to ship to the browser;
  everything else stays server-only and is never referenced from a Client Component
- Named exports for components; default export reserved for `page.tsx`/`layout.tsx`/`loading.tsx`/`error.tsx` (Next.js requirement)
- Co-locate a component's test next to the component, not in a parallel `__tests__` tree

## Testing

- Unit/component tests: Vitest + React Testing Library — see `skills/frontend/testing-frontend`
- E2E tests: Playwright — see `skills/frontend/testing-frontend`
- Test naming: `describe('<Component>')` + `it('<does X> when <condition>')`

## Git

- Conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`
- One feature per PR, squash merge to main
- Run `pnpm typecheck && pnpm lint && pnpm test` before pushing

## Do NOT

- Do not mark a whole page/layout `'use client'` for one interactive child — push it to the leaf.
- Do not put a server-only secret behind `NEXT_PUBLIC_*` — it ships to every browser.
- Do not fetch data with a hand-rolled `useEffect` — use TanStack Query (client) or a direct
  `fetch`/data call in a Server Component.
- Do not put business logic inside a component that's also handling layout/presentation — extract it.
- Do not commit `.env.local` or any file containing real secrets.
- Do not use `any` or disable `strict` mode to silence a type error.
