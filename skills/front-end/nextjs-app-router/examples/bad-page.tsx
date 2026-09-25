// BAD - whole page forced client-side for one handler, unconfigured fetch, raw <img>, no metadata.
'use client';

import { useEffect, useState } from 'react';

export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    fetch(`https://api.example.com/products/${params.id}`)
      .then((res) => res.json())
      .then(setProduct);
  }, [params.id]);

  if (!product) return <p>Loading...</p>;

  return (
    <div>
      <title>{product.name}</title>
      <img src={product.imageUrl} alt={product.name} />
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <button onClick={() => addToCart(product.id)}>Add to cart</button>
    </div>
  );
}
