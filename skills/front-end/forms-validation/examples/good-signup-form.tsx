// GOOD - Zod schema drives RHF validation, accessible error wiring, autoComplete, submit guard.
'use client';

import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const signupSchema = z.object({
  email: z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type SignupFormValues = z.infer<typeof signupSchema>;

export function SignupForm({ onSubmit }: { onSubmit: (values: SignupFormValues) => Promise<void> }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormValues>({ resolver: zodResolver(signupSchema) });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        autoComplete="email"
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? 'email-error' : undefined}
        {...register('email')}
      />
      {errors.email && (
        <p id="email-error" role="alert">
          {errors.email.message}
        </p>
      )}

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        autoComplete="new-password"
        aria-invalid={!!errors.password}
        aria-describedby={errors.password ? 'password-error' : undefined}
        {...register('password')}
      />
      {errors.password && (
        <p id="password-error" role="alert">
          {errors.password.message}
        </p>
      )}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating account…' : 'Sign up'}
      </button>
    </form>
  );
}
