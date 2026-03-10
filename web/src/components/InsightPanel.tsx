"use client";
import clsx from 'clsx';

interface Props {
  habit: { id: string; name: string } | null;
  suggestion: string;
  loading: boolean;
}

export default function InsightPanel({ habit, suggestion, loading }: Props) {
  if (!habit) return null;

  return (
    <section className="mt-8 p-6 bg-card rounded-lg shadow border border-border">
      <h2 className="text-2xl font-bold mb-4 text-foreground">
        AI Coaching for {habit.name}
      </h2>
      {loading ? (
        <p className="text-muted">Generating personalized suggestion…</p>
      ) : (
        <p className={clsx('text-foreground')}>{suggestion}</p>
      )}
    </section>
  );
}
