import { getInsights } from '@/lib/data-loader';
import { ArrowRight, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

/**
 * Research Insights Page
 *
 * Answers key questions about AI-IDE architecture with comparisons
 */

export default async function InsightsPage() {
  const insights = await getInsights();

  // Extract comparison data
  const streamingRepos = insights.filter(i => i.llm_strategy.streaming);
  const toolCallingRepos = insights.filter(i => i.llm_strategy.tool_calling);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
          Research Insights
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Key findings and architectural comparisons across AI-IDE projects
        </p>
      </div>

      {/* Key Question 1: Streaming */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Should I implement streaming responses?
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="font-semibold text-green-600 dark:text-green-400 mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" />
              Repos Using Streaming ({streamingRepos.length}/{insights.length})
            </h3>
            <ul className="space-y-2">
              {streamingRepos.map(repo => (
                <li key={repo.repo_id} className="text-gray-700 dark:text-gray-300">
                  <a href={`/repos/${repo.repo_id}/`} className="hover:text-blue-600 hover:underline">
                    {repo.repo_id}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-gray-600 dark:text-gray-400 mb-3 flex items-center gap-2">
              <XCircle className="w-5 h-5" />
              Not Using Streaming
            </h3>
            <ul className="space-y-2">
              {insights.filter(i => !i.llm_strategy.streaming).map(repo => (
                <li key={repo.repo_id} className="text-gray-700 dark:text-gray-300">
                  <a href={`/repos/${repo.repo_id}/`} className="hover:text-blue-600 hover:underline">
                    {repo.repo_id}
                  </a>
                  {repo.architecture_style === 'cli-agent' && (
                    <span className="ml-2 text-xs text-gray-500">(CLI - less critical)</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
            Recommendation
          </h4>
          <p className="text-blue-800 dark:text-blue-200 mb-2">
            <strong>For GUI/IDE extensions:</strong> Streaming is worth the complexity. It provides
            instant feedback and significantly better perceived performance.
          </p>
          <p className="text-blue-800 dark:text-blue-200">
            <strong>For CLI tools:</strong> Optional. Batch responses are simpler and acceptable
            for non-interactive workflows.
          </p>
        </div>
      </div>

      {/* Key Question 2: Tool Calling */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Should I implement tool/function calling?
        </h2>

        <div className="mb-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
              {toolCallingRepos.length}/{insights.length}
            </div>
            <div className="text-gray-700 dark:text-gray-300">
              repositories implement tool calling
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {insights.map(repo => (
              <div
                key={repo.repo_id}
                className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
              >
                <div>
                  <a
                    href={`/repos/${repo.repo_id}/`}
                    className="font-semibold text-gray-900 dark:text-white hover:text-blue-600 hover:underline"
                  >
                    {repo.repo_id}
                  </a>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {repo.architecture_style}
                  </p>
                </div>
                <div>
                  {repo.llm_strategy.tool_calling ? (
                    <span className="flex items-center gap-2 text-green-600 dark:text-green-400">
                      <CheckCircle2 className="w-5 h-5" />
                      Enabled
                    </span>
                  ) : (
                    <span className="flex items-center gap-2 text-gray-400">
                      <XCircle className="w-5 h-5" />
                      Not used
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
          <h4 className="font-semibold text-amber-900 dark:text-amber-300 mb-2 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Recommendation
          </h4>
          <p className="text-amber-800 dark:text-amber-200 mb-2">
            <strong>High value but experimental:</strong> Tool calling enables powerful agentic
            workflows (file operations, running tests, searching code).
          </p>
          <p className="text-amber-800 dark:text-amber-200">
            <strong>Tradeoff:</strong> Adds significant complexity. Requires careful validation
            to prevent LLM hallucinating dangerous tool calls. Start with read-only tools.
          </p>
        </div>
      </div>

      {/* Comparative Matrix */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Feature Comparison Matrix
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Repository
                </th>
                <th className="text-center py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Architecture
                </th>
                <th className="text-center py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Streaming
                </th>
                <th className="text-center py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Tool Calling
                </th>
                <th className="text-center py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Providers
                </th>
                <th className="text-center py-3 px-4 font-semibold text-gray-900 dark:text-white">
                  Patterns
                </th>
              </tr>
            </thead>
            <tbody>
              {insights.map(repo => (
                <tr
                  key={repo.repo_id}
                  className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900"
                >
                  <td className="py-3 px-4">
                    <a
                      href={`/repos/${repo.repo_id}/`}
                      className="font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                    >
                      {repo.repo_id}
                    </a>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-sm px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
                      {repo.architecture_style}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center">
                    {repo.llm_strategy.streaming ? (
                      <CheckCircle2 className="w-5 h-5 text-green-500 mx-auto" />
                    ) : (
                      <XCircle className="w-5 h-5 text-gray-300 mx-auto" />
                    )}
                  </td>
                  <td className="py-3 px-4 text-center">
                    {repo.llm_strategy.tool_calling ? (
                      <CheckCircle2 className="w-5 h-5 text-green-500 mx-auto" />
                    ) : (
                      <XCircle className="w-5 h-5 text-gray-300 mx-auto" />
                    )}
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-sm">
                      {repo.llm_strategy.providers.length || 0}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-sm">
                      {repo.patterns.length}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Emerging Standards */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Emerging Standards
        </h2>

        <div className="space-y-4">
          {streamingRepos.length >= 2 && (
            <div className="flex items-start gap-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
              <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-green-900 dark:text-green-300 mb-1">
                  Streaming Responses
                </h3>
                <p className="text-green-800 dark:text-green-200 text-sm">
                  <strong>Status:</strong> Emerging standard ({streamingRepos.length}/{insights.length} adoption)
                  <br />
                  <strong>Recommendation:</strong> Safe to adopt for GUI-based tools. Well-proven pattern.
                </p>
              </div>
            </div>
          )}

          {toolCallingRepos.length === 1 && (
            <div className="flex items-start gap-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-yellow-900 dark:text-yellow-300 mb-1">
                  Tool/Function Calling
                </h3>
                <p className="text-yellow-800 dark:text-yellow-200 text-sm">
                  <strong>Status:</strong> Experimental ({toolCallingRepos.length}/{insights.length} adoption)
                  <br />
                  <strong>Recommendation:</strong> High potential but unproven at scale. Proceed with caution.
                </p>
              </div>
            </div>
          )}

          <div className="flex items-start gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <ArrowRight className="w-6 h-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-1">
                Context Optimization
              </h3>
              <p className="text-blue-800 dark:text-blue-200 text-sm">
                <strong>Status:</strong> Critical challenge, no consensus yet
                <br />
                <strong>Observation:</strong> Each repo uses different strategies. This is the #1
                architectural challenge in AI-IDEs.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-4">
        <a
          href="/"
          className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          ← Back to Dashboard
        </a>
        <a
          href="/patterns/"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          View Pattern Details →
        </a>
      </div>
    </div>
  );
}
