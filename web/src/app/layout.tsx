import '@/app/globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full scroll-smooth">
      <body className="min-h-screen bg-gradient-to-b from-background to-muted text-foreground font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
