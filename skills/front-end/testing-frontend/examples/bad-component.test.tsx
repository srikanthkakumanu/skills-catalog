// BAD - test-id-only queries (not an accessibility check, brittle), asserts internal state instead of behavior.
import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Counter } from './counter';

describe('Counter', () => {
  it('increments count', () => {
    const { container, getByTestId } = render(<Counter />);
    const button = getByTestId('increment-button');
    button.click();

    // Reaches into implementation detail instead of asserting the visible outcome
    const instance = (container as unknown as { _reactInternals: { stateNode: { state: { count: number } } } });
    expect(instance._reactInternals.stateNode.state.count).toBe(1);
  });
});
