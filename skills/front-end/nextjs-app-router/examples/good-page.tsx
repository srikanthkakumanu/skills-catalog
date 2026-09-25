// GOOD - Server Component page, explicit cache intent, next/image, generateMetadata, minimal client leaf.
import Image from 'next/image';
import type { Metadata } from 'next';
import { AddToCartButton } from './add-to-cart-button';

async function getProduct(id: string): Promise<Product> {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 60 },
  });
  if (!res.ok) throw new Error('Failed to fetch product');
  return res.json();
}

export async function generateMetadata({
  params,
}: {
  params: { id: string };
}): Promise<Metadata> {
  const product = await getProduct(params.id);
  return { title: product.name, description: product.description };
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <div>
      <Image src={product.imageUrl} alt={product.name} width={480} height={480} />
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  );
}
