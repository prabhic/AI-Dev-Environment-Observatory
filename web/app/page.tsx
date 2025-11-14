import { getInsights, getMeta } from '@/lib/data-loader';
import InsightCard from '@/components/InsightCard';
import { Database, GitBranch, TrendingUp } from 'lucide-react';

export default async function HomePage() {
  const insights = await getInsights();
  const meta = await getMeta();

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
        <h1 className="text-4xl font-bold mb-3">
          Welcome to the AI-IDE Observatory
        </h1>
        <p className="text-lg text-blue-100 mb-6">
          Exploring the architecture and evolution of AI-powered development environments
        </p>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6">
          <div className="bg-white/10 backdrop-blur rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <Database className="w-6 h-6" />
              <span className="text-2xl font-bold">{meta.total_repos}</span>
            </div>
            <div className="text-blue-100">Repositories Analyzed</div>
          </div>

          <div className="bg-white/10 backdrop-blur rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <GitBranch className="w-6 h-6" />
              <span className="text-2xl font-bold">
                {insights.reduce((sum, i) => sum + i.patterns.length, 0)}
              </span>
            </div>
            <div className="text-blue-100">Patterns Discovered</div>
          </div>

          <div className="bg-white/10 backdrop-blur rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <TrendingUp className="w-6 h-6" />
              <span className="text-2xl font-bold">v{meta.version}</span>
            </div>
            <div className="text-blue-100">Analysis Version</div>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="text-sm text-gray-600 dark:text-gray-400">
        Last updated: {new Date(meta.last_updated).toLocaleString()}
      </div>

      {/* Repositories Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Repository Insights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {insights.map((insight) => (
            <InsightCard key={insight.repo_id} insight={insight} />
          ))}
        </div>
      </div>

      {/* About Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          About This Observatory
        </h2>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-gray-700 dark:text-gray-300 mb-4">
            The AI-IDE Observatory is a self-evolving research platform that analyzes the architecture
            of AI-powered integrated development environments. By combining static analysis with
            LLM-powered insights, we uncover patterns, best practices, and evolutionary trends across
            the ecosystem.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                What We Analyze
              </h3>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1">
                <li>Architectural patterns</li>
                <li>LLM integration strategies</li>
                <li>Code organization</li>
                <li>Tool calling approaches</li>
                <li>Context management</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                Growth Path
              </h3>
              <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1">
                <li>Auto-discovery of new repos</li>
                <li>Continuous monitoring</li>
                <li>Evolution tracking over time</li>
                <li>Community contributions</li>
                <li>Research paper generation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
