---
name: styling-tailwind
description: >
  Use when styling components with Tailwind CSS v4 — CSS-first @theme configuration, extracting
  variant helpers instead of long duplicated className strings, design tokens for dark mode, or
  gating animation behind prefers-reduced-motion. Triggers on: Tailwind, className, @theme,
  dark mode, design tokens.
---

# Styling with Tailwind CSS v4

Tailwind CSS v4 is CSS-first — theme customization lives in a `@theme` block inside a CSS file, not
a `tailwind.config.js`.

## CSS-First Theme Tokens

```css
/* app/globals.css */
@import 'tailwindcss';

@theme {
  --color-brand-500: oklch(0.6 0.15 250);
  --color-danger-500: oklch(0.55 0.22 25);
  --font-display: 'Inter', sans-serif;
  --radius-card: 0.75rem;
}
```

A ready-to-copy starter token file is in `templates/theme.css`.

## Design Tokens, Not Hardcoded Colors

Hardcoded hex/rgb values in a `className` can't respond to a theme change (dark mode, brand
re-skin). Reference `@theme` tokens through Tailwind's generated utility classes instead.

```tsx
// Bad — hardcoded color bypasses the theme system entirely
<div className="bg-[#3b82f6] text-white">

// Good — theme token; changes everywhere it's used when the token changes
<div className="bg-brand-500 text-white">
```

## Extract a Variant Helper Instead of a Long className String

A long, duplicated `className` string across every usage of a component is unmaintainable and
error-prone. Extract variants with `class-variance-authority` (`cva`) or `tailwind-variants`.

```tsx
// Bad — every button call site repeats and can drift from every other call site
<button className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50">

// Good — one definition, consistent everywhere
import { cva } from 'class-variance-authority';

const buttonVariants = cva('inline-flex items-center rounded-md px-4 py-2 disabled:opacity-50', {
  variants: {
    variant: {
      primary: 'bg-brand-500 text-white hover:bg-brand-600',
      danger: 'bg-danger-500 text-white hover:bg-danger-600',
    },
  },
});

<button className={buttonVariants({ variant: 'primary' })}>
```

For combining conditional classes without a variant system, use `clsx` + `tailwind-merge` (as
`cn(...)`) so conflicting utility classes resolve predictably instead of both being emitted.

## Gate Animation Behind prefers-reduced-motion

An unconditional CSS animation/transition ignores users who've set their OS to reduce motion —
gate it with Tailwind's `motion-safe:`/`motion-reduce:` variants.

```tsx
// Bad — animates regardless of the user's OS-level motion preference
<div className="animate-bounce">

// Good — respects prefers-reduced-motion automatically
<div className="motion-safe:animate-bounce">
```

## Dark Mode via Theme Tokens, Not Duplicated Classes

Define light/dark values for the same token rather than sprinkling `dark:` variants on every
individual utility across the codebase.

```css
@theme {
  --color-surface: oklch(1 0 0);
}
@media (prefers-color-scheme: dark) {
  @theme {
    --color-surface: oklch(0.2 0 0);
  }
}
```

## Official sources

- Tailwind CSS v4 docs: https://tailwindcss.com/docs
- `@theme` directive: https://tailwindcss.com/docs/theme
- `class-variance-authority`: https://cva.style/docs
- Adapted from Vercel's `web-design-guidelines` Animation, Typography, and Dark Mode rule
  categories: https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent hardcodes a hex/rgb color in a `className` — reference a `@theme` token instead so dark mode/re-theming works.
- Agent repeats a long `className` string across every call site of a component — extract a `cva`/`tailwind-variants` helper.
- Agent adds an unconditional CSS animation — gate with `motion-safe:`/`motion-reduce:` for `prefers-reduced-motion` users.
- Agent creates a `tailwind.config.js` for v4 theme customization — use the CSS-first `@theme` block instead.
- Agent sprinkles `dark:` on every individual utility — define light/dark values for the same token once instead.
- Agent combines conditional classes with string concatenation — use `clsx`/`tailwind-merge` so conflicting utilities resolve predictably.
