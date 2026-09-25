// GOOD - useQuery: correct cache key, automatic caching/dedup, explicit staleTime, no manual loading/error state.
'use client';

import { useQuery } from '@tanstack/react-query';

async function fetchUser(userId: string): Promise<User> {
  const res = await fetch(`/api/users/${userId}`);
  if (!res.ok) throw new Error('Failed to fetch user');
  return res.json();
}

export function UserProfile({ userId }: { userId: string }) {
  const { data: user, isPending, isError, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 60_000,
  });

  if (isPending) return <p>Loading...</p>;
  if (isError) return <p>Error: {error.message}</p>;
  return <div>{user.name}</div>;
}
