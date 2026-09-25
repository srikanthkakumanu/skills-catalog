// BAD - boolean-prop explosion allows invalid combinations, and forwardRef is unneeded ceremony in React 19.
import { forwardRef } from 'react';

type CardProps = {
  isHighlighted?: boolean;
  isDanger?: boolean;
  isCompact?: boolean;
  isElevated?: boolean;
  children: React.ReactNode;
};

// Nothing stops isHighlighted={true} isDanger={true} at the type level, and every new
// visual state means another boolean — this doesn't scale past 3-4 states.
export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ isHighlighted, isDanger, isCompact, isElevated, children }, ref) => {
    const classes = [
      'card',
      isHighlighted && 'card--highlighted',
      isDanger && 'card--danger',
      isCompact && 'card--compact',
      isElevated && 'card--elevated',
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div ref={ref} className={classes}>
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';
