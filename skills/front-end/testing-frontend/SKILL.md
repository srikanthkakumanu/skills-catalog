---
name: testing-frontend
description: >
  Use when writing frontend tests of any kind — unit, component, or end-to-end. Covers Vitest +
  React Testing Library query priority and behavior-focused assertions, MSW-mocked integration
  tests, and Playwright end-to-end tests with role-based locators. Mirrors testing-pyramid's
  unit/slice/integration split for the frontend stack.
---

# Frontend Testing (Vitest + React Testing Library + Playwright)

## Structure

```
Unit/Component Tests  — Vitest + React Testing Library, no network        (70%)
Integration Tests     — component trees + MSW-mocked network              (20%)
E2E Tests              — Playwright, real browser, full stack             (10%)
```

## Query Priority — Role Over Test ID

React Testing Library's query priority exists to keep tests resilient to markup changes and to
double as an accessibility check: if `getByRole` can't find an element, an assistive-technology
user likely can't either.

Priority: `getByRole` (with an accessible name) → `getByLabelText` → `getByPlaceholderText` →
`getByText` → `getByTestId` (last resort only, when no accessible query fits).

```tsx
// Bad — test-id-only query; doesn't verify the element is actually accessible, brittle to refactors
screen.getByTestId('submit-button');

// Good — role query; fails if the button loses its accessible name or role
screen.getByRole('button', { name: /submit/i });
```

## Test Behavior, Not Implementation Detail

Assert on what the user sees/can do, not on internal component state or prop values.

```tsx
// Bad — reaches into component internals; breaks on any refactor even when behavior is unchanged
expect(wrapper.state('isOpen')).toBe(true);

// Good — asserts the user-visible outcome
await userEvent.click(screen.getByRole('button', { name: /open menu/i }));
expect(screen.getByRole('menu')).toBeVisible();
```

## Component Test with user-event

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { SignupForm } from './signup-form';

describe('SignupForm', () => {
  it('shows a validation error for an invalid email', async () => {
    const user = userEvent.setup();
    render(<SignupForm onSubmit={vi.fn()} />);

    await user.type(screen.getByRole('textbox', { name: /email/i }), 'not-an-email');
    await user.click(screen.getByRole('button', { name: /sign up/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent(/valid email/i);
  });
});
```

## Integration Test — Mock the Network, Not the Query Client

Mock at the network boundary (MSW) rather than mocking `useQuery` itself, and give each test a
fresh `QueryClient` so cached data from one test can't leak into the next.

```tsx
function renderWithQueryClient(ui: React.ReactElement) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
}
```

## E2E — Role-Based Locators, No Arbitrary Waits

```ts
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/cart');
  await page.getByRole('button', { name: 'Checkout' }).click();
  await page.getByRole('textbox', { name: 'Card number' }).fill('4242424242424242');
  await page.getByRole('button', { name: 'Pay now' }).click();

  await expect(page.getByRole('heading', { name: 'Order confirmed' })).toBeVisible();
});
```

Never use `page.waitForTimeout(n)` to work around a flaky assertion — Playwright's `expect(...)`
assertions already auto-retry until the condition is true or the test times out. A starter
Playwright config is in `templates/playwright.config.ts`.

## Official sources

- React Testing Library query priority: https://testing-library.com/docs/queries/about/#priority
- Vitest: https://vitest.dev/
- Playwright best practices: https://playwright.dev/docs/best-practices
- MSW: https://mswjs.io/
- Mirrors this catalog's `testing-pyramid` skill's unit/slice/integration split for the backend.

## Gotchas

- Agent reaches for `getByTestId` first — try `getByRole` with an accessible name first; it's both more resilient and an accessibility check.
- Agent asserts on internal component state/props — assert on what the user sees or can interact with instead.
- Agent shares one `QueryClient` instance across tests — create a fresh one per test to avoid cache bleed.
- Agent mocks `useQuery` directly — mock the network with MSW instead, so the real query logic is still exercised.
- Agent uses `page.waitForTimeout(n)` in a Playwright test — use an auto-retrying `expect(...)` assertion instead.
- Agent writes E2E tests for cases a component test already covers — reserve E2E for cross-page/critical-path flows; keep the pyramid bottom-heavy.
