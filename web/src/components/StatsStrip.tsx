"use client";
import clsx from 'clsx';

interface Props {
  totalHabits: number;
}

export default function StatsStrip({ totalHabits }: Props) {
  return (
    <div className={clsx('flex justify-center gap-8 py-4 bg-card rounded-lg shadow') }>
      <div className="text-center">
        <p className="text-2xl font-semibold text-primary">{totalHabits}</p>
        <p className="text-sm text-muted">Habits tracked</p>
      </div>
      {/* Placeholder for future metrics */}
      <div className="text-center">
        <p className="text-2xl font-semibold text-primary">0</p>
        <p className="text-sm text-muted">Current streak</p>
      </div>
    </div>
  );
}
