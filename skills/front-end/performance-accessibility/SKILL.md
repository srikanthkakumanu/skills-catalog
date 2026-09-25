---
name: performance-accessibility
description: >
  Use when reviewing or optimizing bundle size, re-render cost, list rendering performance, or
  accessibility (semantic HTML, keyboard reachability, focus visibility, ARIA). Covers dynamic
  imports for heavy/rarely-used components, avoiding barrel-file over-import, list virtualization,
  and WCAG-baseline component patterns.
---

# Performance and Accessibility

## Dynamic Import Heavy or Rarely-Used Components

A component only shown behind an interaction (a modal, a rich editor, a chart library) shouldn't be
in the initial bundle.

```tsx
// Bad — the chart library ships in the main bundle even though most visits never open it
import { AnalyticsChart } from './analytics-chart';

// Good — loaded only when actually rendered
import dynamic from 'next/dynamic';
const AnalyticsChart = dynamic(() => import('./analytics-chart'), { ssr: false });
```

## Avoid Barrel-File Over-Import

Importing from a package's barrel `index.ts` can pull in far more than what's used, since bundlers
can't always tree-shake through re-exports.

```tsx
// Bad — may pull the entire icon set into the bundle depending on the package's export shape
import { ChevronDownIcon } from 'some-icon-library';

// Good — import the specific module directly
import ChevronDownIcon from 'some-icon-library/icons/chevron-down';
```

## Memoize Only When a Measured Cost Justifies It

`useMemo`/`useCallback`/`React.memo` are not free — they add a comparison cost every render. Reach
for them when profiling shows an expensive computation or a re-render that's actually visible as
jank, not as a default habit on every component.

## Virtualize Long Lists

Rendering hundreds of DOM nodes for a long list tanks initial render and scroll performance —
virtualize so only visible rows mount.

```tsx
// Bad — renders all 1000 rows into the DOM regardless of what's visible
{items.map((item) => <Row key={item.id} item={item} />)}

// Good — only visible rows are mounted
import { useVirtualizer } from '@tanstack/react-virtual';
// ...configure a virtualizer against a scroll container, render only virtualItems
```

## Semantic HTML Over div+onClick

A `<div onClick>` is not keyboard-reachable, has no accessible role, and gets no focus outline by
default. Use the element that already has the right semantics.

```tsx
// Bad — not focusable, not activatable with Enter/Space, no accessible role
<div onClick={handleClick}>Delete</div>

// Good — keyboard-reachable, correct role, focus-visible by default
<button type="button" onClick={handleClick}>Delete</button>
```

## Preserve or Replace the Focus Outline — Never Remove It

Removing `outline` without a visible replacement leaves keyboard users with no way to see where
focus is.

```css
/* Bad — focus becomes invisible for keyboard users */
button:focus { outline: none; }

/* Good — customized but still visible */
button:focus-visible { outline: 2px solid var(--color-brand-500); outline-offset: 2px; }
```

## Official sources

- Web Vitals: https://web.dev/articles/vitals
- WCAG 2.2 quick reference: https://www.w3.org/WAI/WCAG22/quickref/
- `next/dynamic`: https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading
- Adapted from Vercel's `react-best-practices` bundle/rendering rule categories (`bundle-dynamic-imports`,
  `bundle-barrel-imports`, `rendering-content-visibility`) and `web-design-guidelines` Accessibility
  and Focus States categories: https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent ships a heavy, rarely-used component in the initial bundle — dynamic-import it instead.
- Agent imports from a package's barrel `index.ts` for one icon/utility — import the specific module directly.
- Agent wraps every component in `React.memo`/`useMemo` by default — only memoize where a measured cost justifies it.
- Agent renders hundreds of list rows unvirtualized — virtualize long lists.
- Agent uses `<div onClick>` for an interactive element — use `<button>` (or the element with the correct native semantics).
- Agent removes `outline: none` without a `focus-visible` replacement — keyboard users lose all indication of focus.
- Agent omits an `aria-label` on an icon-only button — screen reader users get no accessible name.
