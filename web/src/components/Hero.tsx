"use client";
import { Inter } from 'next/font/google';
import Link from 'next/link';

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '600', '700']
});

export default function Hero() {
  return (
    <section className="text-center py-16 md:py-24" style={inter.style}>
      <h1 className="text-4xl md:text-5xl font-bold text-primary mb-4">
        TriHabit
      </h1>
      <p className="text-xl md:text-2xl text-foreground mb-6 max-w-2xl mx-auto">
        Focus on what matters most with AI‑guided habit tracking for busy professionals.
      </p>
      <Link
        href="#"
        className="inline-block bg-accent text-white px-6 py-3 rounded-lg hover:bg-accent/90 transition"
      >
        Get Started
      </Link>
    </section>
  );
}
