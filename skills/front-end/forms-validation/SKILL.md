---
name: forms-validation
description: >
  Use when building forms with client-side validation — React Hook Form + Zod schemas, sharing one
  schema between client validation and a Server Action, accessible error display, autoComplete
  wiring, or submission/loading state. Triggers on: React Hook Form, Zod, zodResolver, form
  validation, accessible forms.
---

# Forms and Validation (React Hook Form + Zod)

A Zod schema is the single source of truth for a form's shape — the same schema validates on the
client (via `zodResolver`) and re-validates on the server (in the Server Action), so the two never
drift out of sync.

## Schema-Driven Form

```tsx
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const signupSchema = z.object({
  email: z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type SignupFormValues = z.infer<typeof signupSchema>;

function SignupForm({ onSubmit }: { onSubmit: (values: SignupFormValues) => Promise<void> }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormValues>({ resolver: zodResolver(signupSchema) });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <FormField
        label="Email"
        error={errors.email?.message}
        inputProps={{ ...register('email'), type: 'email', autoComplete: 'email' }}
      />
      <FormField
        label="Password"
        error={errors.password?.message}
        inputProps={{ ...register('password'), type: 'password', autoComplete: 'new-password' }}
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating account…' : 'Sign up'}
      </button>
    </form>
  );
}
```

A ready-to-copy accessible field wrapper (`FormField` above) is in `templates/FormField.tsx`.

## Re-Validate the Same Schema on the Server

Client validation is a UX convenience, never a security boundary — a Server Action must re-validate
with the identical schema, because the client can be bypassed entirely.

```tsx
// app/signup/actions.ts
'use server';

export async function signup(formData: FormData) {
  const parsed = signupSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }
  await createUser(parsed.data);
}
```

## Accessible Error Wiring

Every field with an error needs `aria-invalid` and `aria-describedby` pointing at the error message
element — a visually-adjacent red message with no ARIA wiring is invisible to a screen reader.

```tsx
<input
  id="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
  {...register('email')}
/>
{errors.email && (
  <p id="email-error" role="alert">
    {errors.email.message}
  </p>
)}
```

## autoComplete on Every Field

Every input that maps to a standard browser autofill category (`email`, `given-name`,
`current-password`, `new-password`, etc.) needs the matching `autoComplete` attribute — omitting it
silently disables autofill and forces users to retype.

## Submission State

Use `formState.isSubmitting` (RHF) or `useFormStatus` (Server Action `<form>`) to disable the submit
control and show progress — never allow a double-submit from an unguarded button.

## Official sources

- React Hook Form: https://react-hook-form.com/
- Zod: https://zod.dev/
- `@hookform/resolvers`: https://github.com/react-hook-form/resolvers
- Adapted from Vercel's `web-design-guidelines` Forms rule category (autocomplete, validation,
  error handling): https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent hand-writes per-field validation logic instead of a Zod schema — one schema shared client+server prevents drift.
- Agent trusts client-side validation as the only check — a Server Action must re-validate the same schema.
- Agent shows an error message with no `aria-describedby`/`aria-invalid` — screen reader users get no indication which field failed.
- Agent omits `autoComplete` on standard fields (email, password, name) — browser autofill silently breaks.
- Agent leaves the submit button enabled during submission — guard with `isSubmitting`/`useFormStatus` to prevent double-submit.
- Agent uses `useState` per field instead of React Hook Form — loses validation, dirty/touched tracking, and re-render optimization RHF provides via uncontrolled inputs.
