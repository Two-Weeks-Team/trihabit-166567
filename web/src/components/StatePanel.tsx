"use client";
interface Props {
  type: 'loading' | 'empty' | 'error' | 'success';
  message?: string;
}

export default function StatePanel({ type, message }: Props) {
  const defaults: Record<string, string> = {
    loading: 'Loading…',
    empty: 'No data to display.',
    error: 'An error occurred.',
    success: 'Operation successful.'
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p className="text-lg text-muted">{message || defaults[type]}</p>
    </div>
  );
}
