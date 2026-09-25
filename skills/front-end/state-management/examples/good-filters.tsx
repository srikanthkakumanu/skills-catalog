// GOOD - filters live in the URL: survive refresh, shareable via link, back/forward work correctly.
'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';

export function ProductFilters() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const status = searchParams.get('status') ?? 'active';

  function handleChange(next: string) {
    const params = new URLSearchParams(searchParams);
    params.set('status', next);
    router.push(`${pathname}?${params.toString()}`);
  }

  return (
    <select value={status} onChange={(e) => handleChange(e.target.value)}>
      <option value="active">Active</option>
      <option value="archived">Archived</option>
    </select>
  );
}
