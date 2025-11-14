import { getInsights } from '@/lib/data-loader';
import { Code2, Zap, Shield, Scale } from 'lucide-react';

/**
 * Decision Framework Page
 *
 * Helps developers make informed architectural decisions
 */

export default async function DecisionsPage() {
  const insights = await getInsights();

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
          Architectural Decision Framework
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Evidence-based recommendations for building AI-powered development tools
        </p>
      </div>

      {/* Decision 1: LLM Response Strategy */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <div className="flex items-start gap-4 mb-6">
          <Zap className="w-8 h-8 text-yellow-500 flex-shrink-0" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Decision: Streaming vs Batch Responses
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              How should I deliver LLM responses to users?
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Option A: Streaming */}
          <div className="border border-blue-300 dark:border-blue-700 rounded-lg p-6">
            <h3 className="text-lg font-bold text-blue-900 dark:text-blue-300 mb-3">
              Option A: Streaming
            </h3>

            <div className="space-y-3 mb-4">
              <div>
                <h4 className="font-semibold text-green-700 dark:text-green-400 text-sm mb-1">
                  Advantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>Instant feedback - better perceived performance</li>
                  <li>Users can stop generation early if wrong direction</li>
                  <li>Feels more interactive and responsive</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-red-700 dark:text-red-400 text-sm mb-1">
                  Disadvantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>More complex implementation (SSE/WebSocket)</li>
                  <li>Harder to retry on errors mid-stream</li>
                  <li>Need buffering for partial responses</li>
                </ul>
              </div>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/30 rounded p-3 text-sm">
              <strong>Evidence:</strong> {insights.filter(i => i.llm_strategy.streaming).length}/
              {insights.length} repos use streaming
              <br />
              <span className="text-blue-700 dark:text-blue-300">
                {insights.filter(i => i.llm_strategy.streaming && i.architecture_style.includes('extension')).length > 0
                  ? '✓ Standard for GUI/IDE extensions'
                  : '• Mixed adoption'}
              </span>
            </div>
          </div>

          {/* Option B: Batch */}
          <div className="border border-gray-300 dark:border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-gray-300 mb-3">
              Option B: Batch Responses
            </h3>

            <div className="space-y-3 mb-4">
              <div>
                <h4 className="font-semibold text-green-700 dark:text-green-400 text-sm mb-1">
                  Advantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>Simpler implementation - single API call</li>
                  <li>Easy to retry entire request on failure</li>
                  <li>Can process complete response atomically</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-red-700 dark:text-red-400 text-sm mb-1">
                  Disadvantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>No feedback until complete (poor UX for long responses)</li>
                  <li>User can't interrupt if wrong direction</li>
                  <li>Feels unresponsive</li>
                </ul>
              </div>
            </div>

            <div className="bg-gray-50 dark:bg-gray-900/30 rounded p-3 text-sm">
              <strong>Evidence:</strong> Used by CLI-focused tools
              <br />
              <span className="text-gray-600 dark:text-gray-400">
                • Acceptable for non-interactive workflows
              </span>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="font-bold text-gray-900 dark:text-white mb-3">
            📊 Recommendation
          </h3>
          <div className="space-y-2 text-gray-800 dark:text-gray-200">
            <p>
              <strong>Choose Streaming if:</strong> You're building a GUI/IDE extension where
              users interact in real-time. The UX improvement is worth the implementation cost.
            </p>
            <p>
              <strong>Choose Batch if:</strong> You're building a CLI tool or automation where
              users don't need instant feedback. Simplicity is more valuable.
            </p>
            <p className="text-sm italic">
              Evidence: All major GUI-based AI-IDEs (Cline, Continue) use streaming. CLI tools can go either way.
            </p>
          </div>
        </div>
      </div>

      {/* Decision 2: Multi-Provider Support */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <div className="flex items-start gap-4 mb-6">
          <Code2 className="w-8 h-8 text-purple-500 flex-shrink-0" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Decision: Single vs Multi-Provider LLM Support
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Should I support multiple LLM providers?
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Option A: Single Provider */}
          <div className="border border-green-300 dark:border-green-700 rounded-lg p-6">
            <h3 className="text-lg font-bold text-green-900 dark:text-green-300 mb-3">
              Option A: Single Provider
            </h3>

            <div className="space-y-3 mb-4">
              <div>
                <h4 className="font-semibold text-green-700 dark:text-green-400 text-sm mb-1">
                  Advantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>Simpler codebase - no abstraction layer needed</li>
                  <li>Can use provider-specific features fully</li>
                  <li>Easier to optimize for one API</li>
                  <li>Less maintenance burden</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-red-700 dark:text-red-400 text-sm mb-1">
                  Disadvantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>Locked into one provider's pricing/limits</li>
                  <li>Users can't use their preferred model</li>
                  <li>Risk if provider changes API/pricing</li>
                </ul>
              </div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/30 rounded p-3 text-sm">
              <strong>Best for:</strong> MVP, B2B where you control infra
            </div>
          </div>

          {/* Option B: Multi-Provider */}
          <div className="border border-blue-300 dark:border-blue-700 rounded-lg p-6">
            <h3 className="text-lg font-bold text-blue-900 dark:text-blue-300 mb-3">
              Option B: Multi-Provider
            </h3>

            <div className="space-y-3 mb-4">
              <div>
                <h4 className="font-semibold text-green-700 dark:text-green-400 text-sm mb-1">
                  Advantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>Users can choose preferred/cheaper model</li>
                  <li>Flexibility if one provider has issues</li>
                  <li>Can optimize different tasks for different models</li>
                  <li>Market positioning advantage</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-red-700 dark:text-red-400 text-sm mb-1">
                  Disadvantages
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300 space-y-1">
                  <li>~40% more code complexity (abstraction layer)</li>
                  <li>Feature parity challenges (not all providers equal)</li>
                  <li>Testing complexity multiplies</li>
                  <li>Harder to optimize prompts across providers</li>
                </ul>
              </div>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/30 rounded p-3 text-sm">
              <strong>Best for:</strong> Consumer product, developer tools
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
          <h3 className="font-bold text-gray-900 dark:text-white mb-3">
            📊 Recommendation
          </h3>
          <div className="space-y-2 text-gray-800 dark:text-gray-200">
            <p>
              <strong>Start with single provider for MVP.</strong> Get core functionality working
              well before adding abstraction complexity.
            </p>
            <p>
              <strong>Add multi-provider support when:</strong>
            </p>
            <ul className="list-disc list-inside ml-4 space-y-1">
              <li>Users explicitly request it</li>
              <li>You have &gt;1000 users and need differentiation</li>
              <li>Provider pricing/limits become an issue</li>
            </ul>
            <p className="text-sm italic">
              Evidence: Continue built multi-provider from start (market positioning). Cline started
              single-provider (get to market fast). Both valid strategies.
            </p>
          </div>
        </div>
      </div>

      {/* Decision 3: Tool Calling */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-8">
        <div className="flex items-start gap-4 mb-6">
          <Shield className="w-8 h-8 text-red-500 flex-shrink-0" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Decision: Implement Tool/Function Calling?
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Should I allow the LLM to execute tools/functions?
            </p>
          </div>
        </div>

        <div className="bg-amber-50 dark:bg-amber-900/20 border-l-4 border-amber-500 p-6 mb-6">
          <h3 className="font-bold text-amber-900 dark:text-amber-300 mb-2">
            ⚠️ High Risk, High Reward
          </h3>
          <p className="text-amber-800 dark:text-amber-200">
            Tool calling enables powerful agentic workflows but introduces security risks.
            Only {insights.filter(i => i.llm_strategy.tool_calling).length}/{insights.length} repos
            currently implement it - this is experimental territory.
          </p>
        </div>

        <div className="space-y-4 mb-6">
          <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
              If Yes: Safety-First Implementation
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-gray-700 dark:text-gray-300">
              <li>
                <strong>Start with read-only tools</strong> (search files, read code, get documentation)
              </li>
              <li>
                <strong>Validate all tool calls</strong> against a whitelist before execution
              </li>
              <li>
                <strong>Sandbox execution</strong> where possible (containerization, permissions)
              </li>
              <li>
                <strong>Require confirmation</strong> for destructive operations (write, delete, run commands)
              </li>
              <li>
                <strong>Log everything</strong> for debugging and security audits
              </li>
            </ol>
          </div>

          <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
              Alternative: Guided Workflows Instead
            </h3>
            <p className="text-gray-700 dark:text-gray-300 mb-3">
              Instead of autonomous tool execution, present LLM suggestions to the user:
            </p>
            <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
              <li>LLM suggests: "Search for API usage in project"</li>
              <li>You generate: Clickable button "Search project"</li>
              <li>User confirms and reviews results</li>
              <li>Lower risk, still powerful</li>
            </ul>
          </div>
        </div>

        <div className="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="font-bold text-gray-900 dark:text-white mb-3">
            📊 Recommendation
          </h3>
          <div className="space-y-2 text-gray-800 dark:text-gray-200">
            <p>
              <strong>For MVP:</strong> Skip tool calling. Focus on core LLM chat/completion first.
            </p>
            <p>
              <strong>Add tool calling when:</strong>
            </p>
            <ul className="list-disc list-inside ml-4 space-y-1">
              <li>Core functionality is stable</li>
              <li>You have resources for security review</li>
              <li>Start with read-only tools and expand gradually</li>
            </ul>
            <p className="text-sm italic mt-3 text-red-700 dark:text-red-300">
              <strong>Warning:</strong> LLMs can hallucinate tool calls with dangerous parameters.
              Never trust tool call suggestions blindly.
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-4">
        <a
          href="/insights/"
          className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          ← Research Insights
        </a>
        <a
          href="/"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Back to Dashboard
        </a>
      </div>
    </div>
  );
}
