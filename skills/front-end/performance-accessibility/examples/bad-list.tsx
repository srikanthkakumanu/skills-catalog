// BAD - unvirtualized 1000-row list, div+onClick (not keyboard-reachable), no focus style.
export function ProductList({ products }: { products: Product[] }) {
  return (
    <div>
      {products.map((product) => (
        <div key={product.id} onClick={() => selectProduct(product.id)} style={{ padding: 8 }}>
          {product.name}
        </div>
      ))}
    </div>
  );
}
