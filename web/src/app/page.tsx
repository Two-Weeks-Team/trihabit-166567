"use client";
import { useEffect, useState } from "react";
import Hero from '@/components/Hero';
import StatsStrip from '@/components/StatsStrip';
import HabitCard from '@/components/HabitCard';
import InsightPanel from '@/components/InsightPanel';
import CollectionPanel from '@/components/CollectionPanel';
import StatePanel from '@/components/StatePanel';
import { fetchHabits, checkInHabit } from '@/lib/api';

interface Habit {
  id: string;
  name: string;
  description?: string;
}

export default function HomePage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedHabit, setSelectedHabit] = useState<Habit | null>(null);
  const [coaching, setCoaching] = useState<string>('');
  const [coachingLoading, setCoachingLoading] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchHabits();
        setHabits(data.habits);
        if (data.habits.length) setSelectedHabit(data.habits[0]);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // fetch coaching when a habit is selected or after a check‑in
  useEffect(() => {
    if (!selectedHabit) return;
    const habitId = selectedHabit.id;
    async function getCoaching() {
      setCoachingLoading(true);
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/habits/${habitId}/coaching`);
        if (!res.ok) throw new Error('Coaching fetch failed');
        const body = await res.json();
        setCoaching(body.suggestion);
      } catch (e: any) {
        setCoaching('Unable to load coaching at this time.');
      } finally {
        setCoachingLoading(false);
      }
    }
    getCoaching();
  }, [selectedHabit]);

  const handleCheckIn = async (habitId: string) => {
    try {
      await checkInHabit(habitId, { date: new Date().toISOString().split('T')[0], notes: '' });
      // refresh coaching for that habit
      setSelectedHabit(habits.find((h) => h.id === habitId) || null);
    } catch (e: any) {
      alert('Check‑in failed: ' + e.message);
    }
  };

  if (loading) return <StatePanel type="loading" />;
  if (error) return <StatePanel type="error" message={error} />;
  if (!habits.length) return <StatePanel type="empty" message="No habits found. Start by adding your three priority habits." />;

  return (
    <main className="container mx-auto px-4 py-8 space-y-12">
      <Hero />
      <StatsStrip totalHabits={habits.length} />
      <section className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {habits.map((habit) => (
          <HabitCard
            key={habit.id}
            habit={habit}
            onCheckIn={() => handleCheckIn(habit.id)}
          />
        ))}
      </section>
      <InsightPanel
        habit={selectedHabit}
        suggestion={coaching}
        loading={coachingLoading}
      />
      <CollectionPanel habits={habits} />
    </main>
  );
}
