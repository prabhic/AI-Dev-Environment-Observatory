import { getInsights } from '@/lib/data-loader';
import { notFound } from 'next/navigation';
import { Code2, FileText, GitBranch, Layers, Sparkles } from 'lucide-react';

interface Props {
  params: {
    slug: string;
  };
}

export async function generateStaticParams() {
  const insights = await getInsights();
  return insights.map((insight) => ({
    slug: insight.repo_id,
  }));
}

export default async function RepoPage({ params }: Props) {
  const insights = await getInsights();
  const insight = insights.find((i) => i.repo_id === params.slug);

  if (!insight) {
    notFound();
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <a href="/" className="text-blue-600 dark:text-blue-400 hover:underline mb-4 inline-block">
          ← Back to Dashboard
        </a>

        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          {insight.repo_id}
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-4">
          {insight.description || `${insight.architecture_style} built with ${insight.primary_language}`}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-sm">
            {insight.architecture_style}
          </span>
          <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full text-sm">
            {insight.primary_language}
          </span>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <Code2 className="w-5 h-5 text-blue-500" />
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              {insight.components.length}
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Components</div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <Layers className="w-5 h-5 text-green-500" />
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              {insight.patterns.length}
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Patterns</div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-5 h-5 text-purple-500" />
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              {insight.analysis_metadata.files_analyzed}
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Files Analyzed</div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="w-5 h-5 text-yellow-500" />
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              {Math.round(insight.analysis_metadata.confidence * 100)}%
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Confidence</div>
        </div>
      </div>

      {/* Key Insights */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-yellow-500" />
          Key Insights
        </h2>
        <ul className="space-y-3">
          {insight.key_insights.map((item, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="text-blue-500 font-bold mt-1">→</span>
              <span className="text-gray-700 dark:text-gray-300">{item}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* LLM Strategy */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          LLM Integration Strategy
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Providers</h3>
            <div className="flex flex-wrap gap-2">
              {insight.llm_strategy.providers.map((provider) => (
                <span
                  key={provider}
                  className="px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded-full text-sm"
                >
                  {provider}
                </span>
              ))}
              {insight.llm_strategy.providers.length === 0 && (
                <span className="text-gray-500 text-sm">None detected</span>
              )}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Features</h3>
            <div className="flex flex-wrap gap-2">
              {insight.llm_strategy.streaming && (
                <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-sm">
                  ✓ Streaming
                </span>
              )}
              {insight.llm_strategy.tool_calling && (
                <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full text-sm">
                  ✓ Tool Calling
                </span>
              )}
            </div>
          </div>

          {insight.llm_strategy.context_optimization && (
            <div className="md:col-span-2">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                Context Optimization
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                {insight.llm_strategy.context_optimization}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Patterns */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <GitBranch className="w-6 h-6 text-green-500" />
          Detected Patterns ({insight.patterns.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insight.patterns.map((pattern, index) => (
            <div
              key={index}
              className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
            >
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                {pattern.name}
              </h3>
              <p className="text-xs text-gray-500 mb-2">{pattern.category}</p>
              <p className="text-sm text-gray-700 dark:text-gray-300">{pattern.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Components */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Key Components ({insight.components.length})
        </h2>
        <div className="space-y-4">
          {insight.components.slice(0, 10).map((component, index) => (
            <div
              key={index}
              className="border-l-4 border-blue-500 pl-4 py-2"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {component.name}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {component.file_path}
                  </p>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                    {component.purpose}
                  </p>
                  {component.key_patterns.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {component.key_patterns.map((pattern, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded text-xs"
                        >
                          {pattern}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs ${
                    component.complexity === 'low'
                      ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                      : component.complexity === 'medium'
                      ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300'
                      : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300'
                  }`}
                >
                  {component.complexity}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dependencies */}
      {insight.key_dependencies.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Key Dependencies
          </h2>
          <div className="flex flex-wrap gap-2">
            {insight.key_dependencies.map((dep, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded text-sm font-mono"
              >
                {dep}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
