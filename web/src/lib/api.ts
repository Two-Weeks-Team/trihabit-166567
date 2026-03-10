export async function fetchHabits() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/habits`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store'
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || 'Failed to fetch habits');
  }
  return res.json();
}

export async function checkInHabit(habitId: string, payload: { date: string; notes?: string }) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/habits/${habitId}/check-in`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || 'Check‑in failed');
  }
  return res.json();
}
