# Next.js 16 · React 19 + TypeScript Frontend

The default browser-facing UI stack — evidence-gated by `tech-stack/SKILL.md` Directive 1. Only
select this playbook once a context's frontend/presentation layer has actually been decomposed in
(a confirmed UI need), never on an FR alone.

## Fits
- **UI channel:** browser-based web application/dashboard/portal confirmed as a bounded context's
  consumer (BRD persona or `detailed-design.md` API Contracts naming a UI-facing boundary)
- **Rendering needs:** mixed static/dynamic content, SEO-relevant pages, streaming UI — Next.js App
  Router (Server Components by default)
- **Server state:** data fetched from a confirmed backend API (see `rest-api/*` playbooks) —
  TanStack Query as the client-side cache
- **Forms:** user input needing client-side and shared validation — React Hook Form + Zod
- **Styling:** utility-first, design-token-driven, dark-mode-capable — Tailwind CSS v4

## Does NOT fit
- No UI-facing consumer evidenced for the context (pure service-to-service/API-only/batch) — don't
  attach this playbook; that's not a mismatch, it's the evidence gate at decomposition (Directive 1)
  saying no frontend layer exists to match a playbook to
- Native mobile delivery — this playbook covers web only; a mobile requirement is off-catalog,
  present tradeoffs rather than forcing this playbook onto it
- A CMS-authored marketing/brochure site with no app-like interactivity — likely over-engineered
  against a static-site generator; flag as off-catalog if that's the *entire* need

## Stack
| Component | Choice |
|---|---|
| Language | TypeScript 5.9.x, strict mode (see `typescript-language-conventions`) |
| Framework | Next.js 16.x, App Router, Turbopack (default dev bundler) |
| UI library | React 19.3.x |
| Server state / data fetching | TanStack Query (`@tanstack/react-query`) 5.103.x |
| Forms & validation | React Hook Form 7.88.x + Zod 4.6.x (via `@hookform/resolvers` ^5.1.0) |
| Styling | Tailwind CSS 4.3.x, CSS-first `@theme` config |
| Testing — unit/component | Vitest 5.0.x + `@testing-library/react` 16.3.x |
| Testing — e2e | Playwright (`@playwright/test`) 1.63.x |
| Runtime | Node.js 24.x (Active LTS) |
| Package manager | pnpm |

## Prerequisites
- `'use client'` only at the smallest interactive leaf — never a whole page/layout
- Every `fetch`/`useQuery` call states an explicit cache/`staleTime` intent — never a bare
  unconfigured `fetch`
- A Zod schema is the single source of truth for a form's shape — never hand-duplicated validation
- `next/image` and `next/font` for every image/font — no raw `<img>`/font `<link>` tags
- WCAG 2.2 AA baseline (semantic HTML, keyboard reachability, visible focus, ARIA wiring) is not
  optional

## Tradeoffs
- Server Components' server/client mental model is a genuine learning curve versus a plain SPA —
  worth it once SEO/streaming/bundle-size matter, overkill for a tiny internal tool with no SEO need
- Fast-moving major-version cadence (Next.js, Zod, Tailwind all ship breaking majors roughly
  yearly) — pin versions deliberately, expect more churn than this catalog's Spring Boot side

## Implementation detail
`implementation-guide` (Phase 7) — react-component-patterns, nextjs-app-router, state-management,
data-fetching, forms-validation, styling-tailwind, testing-frontend, performance-accessibility.
