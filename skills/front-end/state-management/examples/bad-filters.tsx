// BAD - filters live in useState: lost on refresh, not shareable via link, back button does nothing.
'use client';

import { useState } from 'react';

export function ProductFilters({ onChange }: { onChange: (status: string) => void }) {
  const [status, setStatus] = useState('active');

  function handleChange(next: string) {
    setStatus(next);
    onChange(next);
  }

  return (
    <select value={status} onChange={(e) => handleChange(e.target.value)}>
      <option value="active">Active</option>
      <option value="archived">Archived</option>
    </select>
  );
}
