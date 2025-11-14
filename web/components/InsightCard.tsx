import { ArchitecturalInsight } from '@/lib/types';
import { Calendar, Code2, Layers, Sparkles } from 'lucide-react';

interface InsightCardProps {
  insight: ArchitecturalInsight;
}

export default function InsightCard({ insight }: InsightCardProps) {
  return (
    <a
      href={`/repos/${insight.repo_id}/`}
      className="block bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-all hover:border-blue-500"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
            {insight.repo_id}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {insight.architecture_style} • {insight.primary_language}
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <Calendar className="w-4 h-4" />
          {new Date(insight.analyzed_at).toLocaleDateString()}
        </div>
      </div>

      {/* Description */}
      {insight.description && (
        <p className="text-gray-700 dark:text-gray-300 mb-4 line-clamp-2">
          {insight.description}
        </p>
      )}

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="flex items-center gap-2">
          <Code2 className="w-4 h-4 text-blue-500" />
          <div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">
              {insight.components.length}
            </div>
            <div className="text-xs text-gray-500">Components</div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-green-500" />
          <div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">
              {insight.patterns.length}
            </div>
            <div className="text-xs text-gray-500">Patterns</div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-purple-500" />
          <div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">
              {insight.llm_strategy.providers.length || 0}
            </div>
            <div className="text-xs text-gray-500">LLM Providers</div>
          </div>
        </div>
      </div>

      {/* LLM Features */}
      <div className="flex flex-wrap gap-2">
        {insight.llm_strategy.streaming && (
          <span className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded">
            Streaming
          </span>
        )}
        {insight.llm_strategy.tool_calling && (
          <span className="px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded">
            Tool Calling
          </span>
        )}
        {insight.llm_strategy.providers.map(provider => (
          <span key={provider} className="px-2 py-1 text-xs bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded">
            {provider}
          </span>
        ))}
      </div>
    </a>
  );
}
