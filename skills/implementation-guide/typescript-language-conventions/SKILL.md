---
name: typescript-language-conventions
description: >
  TypeScript 5.9 baseline for this catalog's frontend contexts — version/toolchain/build facts and
  language-feature usage guidance (discriminated unions, satisfies, template literal types, utility
  types). Restates tech-stack/stacks/frontend-nextjs-react-typescript.md's constraint; loaded
  unconditionally for every frontend context by implementation-guide, never resolved per-topic.
---
# TypeScript 5.9

Restates the constraint from `tech-stack/stacks/frontend-nextjs-react-typescript.md` identically —
read that file for the decision and its rationale; this file states how `implementation-guide`
applies it, and covers both the version/toolchain facts and language-feature usage guidance in one
place. Next.js-specific project conventions live in `../nextjs-project-conventions/SKILL.md`.

## Version

**TypeScript 5.9.x.** House standard — chosen over TypeScript 7.0's native Go compiler (stable
since July 2026) because full ecosystem compatibility (ESLint's `typescript-eslint` parser,
Vitest's type-checking, Next.js 16's internal type pass) with the native compiler wasn't verified
at the time this baseline was set. Revisit once that chain is confirmed compatible.

## Build

- pnpm (this catalog's house package manager for frontend contexts)
- `tsconfig.json`: `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`
- `moduleResolution: "bundler"`, `module: "esnext"` (Next.js 16 default)

## Runtime

Node.js 24.x, Active LTS.

## Discriminated Unions for Domain State

Model a value's possible shapes as a tagged union rather than one object with a pile of optional
fields — the compiler can then enforce exhaustive handling at every call site.

```typescript
// Bad — every consumer has to guess which fields are valid together
type PaymentResult = {
  status: string;
  authCode?: string;
  reason?: string;
  reference?: string;
};

// Good — a closed, discriminated union
type PaymentResult =
  | { status: 'approved'; authCode: string }
  | { status: 'declined'; reason: string }
  | { status: 'pending'; reference: string };

function describe(result: PaymentResult): string {
  switch (result.status) {
    case 'approved':
      return `Approved: ${result.authCode}`;
    case 'declined':
      return `Declined: ${result.reason}`;
    case 'pending':
      return `Pending: ${result.reference}`;
  }
}
```

## satisfies Over Type Assertions

`satisfies` checks a value against a type without widening or discarding the value's inferred
literal type — an `as` assertion silences the checker instead of using it.

```typescript
// Bad — `as` disables checking entirely; a typo here isn't caught
const config = { theme: 'dar' } as Config;

// Good — checked against Config, but `config.theme` still narrows to the literal 'dark'
const config = { theme: 'dark' } satisfies Config;
```

## Utility Types Over Hand-Duplicated Interfaces

```typescript
// Bad — a hand-duplicated near-copy of CreateUserRequest that drifts as the original changes
type UpdateUserRequest = { name?: string; email?: string };

// Good — derived from the source of truth
type UpdateUserRequest = Partial<Pick<CreateUserRequest, 'name' | 'email'>>;
```

## Template Literal Types for Structured Strings

```typescript
type Route = `/products/${string}` | `/orders/${string}`;
type EventName = `on${Capitalize<'click' | 'hover' | 'focus'>}`;
```

## Do NOT

- Do not use `any` — use `unknown` and narrow, or model the actual shape.
- Do not use a type assertion (`as`) to silence a real type error — fix the underlying type or use `satisfies`.
- Do not hand-duplicate a type that's a subset/variant of an existing one — derive it with `Pick`/`Omit`/`Partial`.
- Do not model a multi-shape value as one object with optional fields — use a discriminated union.
- Do not disable `strict` mode or any of its constituent flags to make a type error go away.
