import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI-IDE Observatory",
  description: "Self-evolving research platform for AI-IDE architecture analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
        <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  🔬 AI-IDE Observatory
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Self-Evolving Research Platform
                </p>
              </div>
              <nav className="flex gap-6">
                <a href="/" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                  Dashboard
                </a>
                <a href="/patterns/" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                  Patterns
                </a>
              </nav>
            </div>
          </div>
        </header>
        <main className="container mx-auto px-6 py-8">
          {children}
        </main>
        <footer className="border-t border-gray-200 dark:border-gray-700 mt-12">
          <div className="container mx-auto px-6 py-6 text-center text-sm text-gray-600 dark:text-gray-400">
            <p>AI-IDE Observatory v1.0 • Built with Next.js, TypeScript, and Anthropic Claude</p>
            <p className="mt-1">A living research platform for understanding AI-IDE evolution</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
