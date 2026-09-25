---
name: front-end
description: >
  Next.js 16 / React 19 / TypeScript 5.9 front-end (frontend or front end) reference covering component composition, App
  Router rendering and data patterns, state management, TanStack Query data fetching, React Hook
  Form + Zod validation, Tailwind CSS styling, Vitest/RTL/Playwright testing, and performance and
  accessibility. Covers 8 topic(s): react-component-patterns, nextjs-app-router, state-management,
  data-fetching, forms-validation, styling-tailwind, testing-frontend, performance-accessibility.
  Resolved by the implementation-guide skill once tech-stack confirms an evidence-gated frontend
  context, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Frontend Skill

Next.js 16 / React 19 / TypeScript 5.9 frontend reference covering component composition, App
Router rendering and data patterns, state management, TanStack Query data fetching, React Hook
Form + Zod validation, Tailwind CSS styling, Vitest/RTL/Playwright testing, and performance and
accessibility.

## Topics

| Topic                                                               | Use when                                                                                                               |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [`react-component-patterns/`](react-component-patterns/SKILL.md)   | Composing React 19 components — compound components, variant props, ref-as-prop, avoiding boolean-prop explosion.     |
| [`nextjs-app-router/`](nextjs-app-router/SKILL.md)                 | Next.js 16 App Router — Server/Client Component boundary, data fetching cache intent, streaming, SEO, Server Actions. |
| [`state-management/`](state-management/SKILL.md)                   | Choosing between UI state, URL state, and server state; avoiding unnecessary re-renders.                               |
| [`data-fetching/`](data-fetching/SKILL.md)                         | TanStack Query setup, query keys, caching, mutations, optimistic updates, parallel fetching.                           |
| [`forms-validation/`](forms-validation/SKILL.md)                   | React Hook Form + Zod schemas, shared client/server validation, accessible error handling.                             |
| [`styling-tailwind/`](styling-tailwind/SKILL.md)                   | Tailwind CSS v4 theming, variant helpers, design tokens, reduced-motion handling.                                      |
| [`testing-frontend/`](testing-frontend/SKILL.md)                   | Vitest + React Testing Library unit/component tests and Playwright end-to-end tests.                                   |
| [`performance-accessibility/`](performance-accessibility/SKILL.md) | Bundle size, re-render cost, list virtualization, semantic HTML, keyboard/focus accessibility.                         |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 8 topic(s) listed above — this skill covers only Next.js 16 / React 19 /
  TypeScript 5.9 frontend concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision (evidence-gated
  per its Directive 1), cited via its playbooks' "Implementation detail" lines.
- Native mobile, static-site/CMS marketing pages, or non-React frontend frameworks — off-catalog.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
