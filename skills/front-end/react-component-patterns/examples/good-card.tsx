// GOOD - one closed variant union makes invalid states unrepresentable; ref is a plain prop (React 19).
type CardVariant = 'default' | 'highlighted' | 'danger';
type CardDensity = 'compact' | 'elevated';

type CardProps = {
  variant?: CardVariant;
  density?: CardDensity;
  children: React.ReactNode;
  ref?: React.Ref<HTMLDivElement>;
};

export function Card({ variant = 'default', density, children, ref }: CardProps) {
  const classes = ['card', `card--${variant}`, density && `card--${density}`]
    .filter(Boolean)
    .join(' ');

  return (
    <div ref={ref} className={classes}>
      {children}
    </div>
  );
}
