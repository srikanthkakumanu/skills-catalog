// Drop-in accessible field wrapper: label + input + ARIA-wired error message.
// Spread register(...) output into inputProps.
type FormFieldProps = {
  label: string;
  error?: string;
  inputProps: React.InputHTMLAttributes<HTMLInputElement>;
};

export function FormField({ label, error, inputProps }: FormFieldProps) {
  const id = inputProps.id ?? inputProps.name;
  const errorId = error ? `${id}-error` : undefined;

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} aria-invalid={!!error} aria-describedby={errorId} {...inputProps} />
      {error && (
        <p id={errorId} role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
