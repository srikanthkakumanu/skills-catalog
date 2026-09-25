// GOOD - variant helper (single source of truth), theme tokens, motion-safe gating.
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center rounded-md px-4 py-2 disabled:opacity-50 motion-safe:transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-brand-500 text-white hover:bg-brand-600',
        danger: 'bg-danger-500 text-white hover:bg-danger-600',
      },
    },
    defaultVariants: { variant: 'primary' },
  }
);

type ButtonProps = React.ComponentProps<'button'> & VariantProps<typeof buttonVariants>;

export function Button({ variant, className, ...props }: ButtonProps) {
  return <button className={buttonVariants({ variant, className })} {...props} />;
}
