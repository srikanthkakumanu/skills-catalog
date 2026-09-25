// GOOD - virtualized rows, semantic <button>, keyboard-reachable with a visible focus ring.
import { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

export function ProductList({ products }: { products: Product[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: products.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 40,
  });

  return (
    <div ref={parentRef} style={{ height: 480, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualRow) => {
          const product = products[virtualRow.index];
          return (
            <button
              key={product.id}
              type="button"
              onClick={() => selectProduct(product.id)}
              className="focus-visible:outline-2 focus-visible:outline-brand-500"
              style={{
                position: 'absolute',
                top: 0,
                transform: `translateY(${virtualRow.start}px)`,
                height: virtualRow.size,
                width: '100%',
              }}
            >
              {product.name}
            </button>
          );
        })}
      </div>
    </div>
  );
}
