"use client";
import { useState } from "react";
import { CheckCircleIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

interface Habit {
  id: string;
  name: string;
  description?: string;
}

interface Props {
  habit: Habit;
  onCheckIn: () => void;
}

export default function HabitCard({ habit, onCheckIn }: Props) {
  const [checking, setChecking] = useState(false);

  const handleClick = async () => {
    setChecking(true);
    try {
      await onCheckIn();
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className={twMerge('bg-card rounded-lg p-4 shadow border border-border') }>
      <h3 className="text-lg font-semibold mb-2 text-foreground">{habit.name}</h3>
      {habit.description && <p className="text-sm text-muted mb-4">{habit.description}</p>}
      {/* Simple progress ring (placeholder) */}
      <svg viewBox="0 0 36 36" className="w-12 h-12 mx-auto mb-4">
        <path
          fill="none"
          stroke="var(--muted)"
          strokeWidth="3"
          d="M18 2.0845
             a 15.9155 15.9155 0 0 1 0 31.831"
        />
        <path
          fill="none"
          stroke="var(--primary)"
          strokeWidth="3"
          strokeDasharray="100, 100"
          d="M18 2.0845
             a 15.9155 15.9155 0 0 1 0 31.831"
        />
        <text x="18" y="20.35" className="fill-foreground text-xs" textAnchor="middle">0%</text>
      </svg>
      <button
        onClick={handleClick}
        disabled={checking}
        className={clsx(
          'w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg transition',
          checking ? 'bg-muted cursor-not-allowed' : 'bg-primary text-white hover:bg-primary/90'
        )}
      >
        <CheckCircleIcon className="h-5 w-5" />
        {checking ? 'Checking…' : 'Check In'}
      </button>
    </div>
  );
}
