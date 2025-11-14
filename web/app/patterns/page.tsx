import { getPatterns } from '@/lib/data-loader';
import { GitBranch, TrendingUp } from 'lucide-react';

export default async function PatternsPage() {
  const patterns = await getPatterns();

  // Group patterns by category
  const patternsByCategory = patterns.reduce((acc, pattern) => {
    if (!acc[pattern.category]) {
      acc[pattern.category] = [];
    }
    acc[pattern.category].push(pattern);
    return acc;
  }, {} as Record<string, typeof patterns>);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
          Cross-Repository Patterns
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Common patterns and architectural approaches across AI-IDE projects
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <GitBranch className="w-6 h-6 text-blue-500" />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {patterns.length}
            </span>
          </div>
          <div className="text-gray-600 dark:text-gray-400">Total Patterns</div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <Layers className="w-6 h-6 text-green-500" />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {Object.keys(patternsByCategory).length}
            </span>
          </div>
          <div className="text-gray-600 dark:text-gray-400">Categories</div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-6 h-6 text-purple-500" />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">
              {patterns.filter(p => p.metadata.prevalence >= 2).length}
            </span>
          </div>
          <div className="text-gray-600 dark:text-gray-400">Shared Patterns</div>
        </div>
      </div>

      {/* Patterns by Category */}
      {Object.entries(patternsByCategory).map(([category, categoryPatterns]) => (
        <div key={category} className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white capitalize">
            {category.replace(/_/g, ' ')}
          </h2>

          <div className="grid grid-cols-1 gap-6">
            {categoryPatterns.map((pattern) => (
              <div
                key={pattern.pattern_id}
                className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {pattern.name}
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300">
                      {pattern.description}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        pattern.metadata.maturity === 'standard'
                          ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                          : pattern.metadata.maturity === 'established'
                          ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                          : 'bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300'
                      }`}
                    >
                      {pattern.metadata.maturity}
                    </span>
                    <span className="text-sm text-gray-500">
                      {pattern.metadata.prevalence} repo{pattern.metadata.prevalence !== 1 ? 's' : ''}
                    </span>
                  </div>
                </div>

                {/* Implementations */}
                <div className="mt-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Implementations:
                  </h4>
                  <div className="space-y-3">
                    {pattern.implementations.map((impl, idx) => (
                      <div
                        key={idx}
                        className="border-l-4 border-blue-500 pl-4 py-2 bg-gray-50 dark:bg-gray-900 rounded-r"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <a
                            href={`/repos/${impl.repo_id}/`}
                            className="font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                          >
                            {impl.repo_id}
                          </a>
                          {impl.maturity && (
                            <span className="text-xs px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">
                              {impl.maturity}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          {impl.approach}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {patterns.length === 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
          <p className="text-yellow-800 dark:text-yellow-200">
            No cross-repository patterns found yet. Run analysis on at least 2 repositories to
            detect patterns.
          </p>
        </div>
      )}
    </div>
  );
}

function Layers({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M4 7l8-4 8 4M4 12l8 4 8-4M4 17l8 4 8-4"
      />
    </svg>
  );
}
