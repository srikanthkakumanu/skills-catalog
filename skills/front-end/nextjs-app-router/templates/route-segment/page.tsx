// Starter Server Component page for a new async route segment.
// Pair with loading.tsx and error.tsx in this same directory.
export default async function Page({ params }: { params: { id: string } }) {
  const data = await fetch(`https://api.example.com/resource/${params.id}`, {
    next: { revalidate: 60 },
  }).then((res) => {
    if (!res.ok) throw new Error('Failed to fetch resource');
    return res.json();
  });

  return (
    <div>
      <h1>{data.title}</h1>
    </div>
  );
}
