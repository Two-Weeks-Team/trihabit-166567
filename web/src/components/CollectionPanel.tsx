"use client";
import clsx from 'clsx';

interface Habit {
  id: string;
  name: string;
}

interface Props {
  habits: Habit[];
}

export default function CollectionPanel({ habits }: Props) {
  return (
    <section className="mt-8">
      <h2 className="text-xl font-semibold mb-3 text-foreground">Your Habits</h2>
      <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {habits.map((h) => (
          <li
            key={h.id}
            className={clsx('bg-card rounded-lg p-4 shadow border border-border')}
          >
            <p className="font-medium text-foreground">{h.name}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
