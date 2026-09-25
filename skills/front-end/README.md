# Frontend Skill

**Next.js 16 / React 19 / TypeScript 5.9 frontend reference covering component composition, App
Router rendering and data patterns, state management, TanStack Query data fetching, React Hook
Form + Zod validation, Tailwind CSS styling, Vitest/RTL/Playwright testing, and performance and
accessibility.**

## Overview

A Next.js 16.x / React 19.x / TypeScript 5.9.x reference collection for frontend concerns,
structured the same way this catalog's Spring Boot reference skills are. It groups 8 topic(s),
each its own self-contained reference with a directive `SKILL.md`, bad-vs-good `examples/`, and
(where applicable) copy-paste `templates/`.

Content is adapted from `vercel-labs/agent-skills` (Vercel's own React/Next.js performance and
design guidelines) and other production-derived skill collections, rewritten into this catalog's
own directive format — see each topic's `## Official sources` section for the upstream references.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `react-component-patterns` | Compound components, variant props, ref-as-prop, avoiding boolean-prop explosion. | `react-component-patterns/` |
| `nextjs-app-router` | Server/Client Component boundary, data fetching cache intent, streaming, SEO, Server Actions. | `nextjs-app-router/` |
| `state-management` | UI state vs URL state vs server state; avoiding unnecessary re-renders. | `state-management/` |
| `data-fetching` | TanStack Query setup, query keys, caching, mutations, optimistic updates, parallel fetching. | `data-fetching/` |
| `forms-validation` | React Hook Form + Zod schemas, shared client/server validation, accessible error handling. | `forms-validation/` |
| `styling-tailwind` | Tailwind CSS v4 theming, variant helpers, design tokens, reduced-motion handling. | `styling-tailwind/` |
| `testing-frontend` | Vitest + React Testing Library unit/component tests and Playwright end-to-end tests. | `testing-frontend/` |
| `performance-accessibility` | Bundle size, re-render cost, list virtualization, semantic HTML, keyboard/focus accessibility. | `performance-accessibility/` |

## When to Use

Invoke this skill directly when working on a Next.js/React/TypeScript project and the task matches
one of the topics above. It is also resolved automatically by the `implementation-guide` skill:
once `tech-stack.md` confirms a context's frontend/presentation layer (evidence-gated — see
`tech-stack/SKILL.md` Directive 1), `implementation-guide` cites the matching topic path here
(`skills/frontend/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project needs a frontend layer at all — that's `tech-stack`'s job.
- Non-React frontend frameworks (Vue, Angular, Svelte), native mobile, or static-site/CMS builds —
  off-catalog; see `tech-stack/stacks/frontend-nextjs-react-typescript.md`'s "Does NOT fit" section.
- Backend/API concerns — see `rest-api/` and `persistence/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill frontend

# Install via file copy
./install.sh --skill frontend --mode copy

# Install to a specific runtime
./install.sh --skill frontend --target claude

# Force-reinstall
./install.sh --skill frontend --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/frontend nextjs app router

react component patterns
tanstack query data fetching
react hook form zod validation
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`react-component-patterns/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`nextjs-app-router/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`state-management/`** — `SKILL.md` (directive), `examples/` (bad vs good), `agents/` where present
- **`data-fetching/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`forms-validation/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`styling-tailwind/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`testing-frontend/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`performance-accessibility/`** — `SKILL.md` (directive), `examples/` (bad vs good), `agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
