// BAD - per-field useState, hand-written validation, no ARIA wiring, no autoComplete, no submit guard.
'use client';

import { useState } from 'react';

export function SignupForm({ onSubmit }: { onSubmit: (values: { email: string; password: string }) => Promise<void> }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email.includes('@')) {
      setEmailError('Invalid email');
      return;
    }
    onSubmit({ email, password });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
      {emailError && <span style={{ color: 'red' }}>{emailError}</span>}
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Sign up</button>
    </form>
  );
}
