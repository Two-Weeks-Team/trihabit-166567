import type { Config } from 'tailwindcss';

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: "var(--primary)",
        accent: "var(--accent)",
        card: "var(--card)",
        muted: "var(--muted)",
        border: "var(--border)",
        success: "var(--success)",
        warning: "var(--warning)"
      },
      borderRadius: {
        radius: "var(--radius)"
      },
      boxShadow: {
        shadow: "var(--shadow)"
      }
    }
  },
  plugins: []
};

export default config;
