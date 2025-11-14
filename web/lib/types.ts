/**
 * TypeScript types for Observatory data
 */

export interface Repository {
  id: string;
  name: string;
  url: string;
  type: string;
  language: string;
  focus_areas: string[];
  analysis_priority: string;
  tags: string[];
}

export interface ComponentAnalysis {
  name: string;
  purpose: string;
  file_path: string;
  key_patterns: string[];
  complexity: "low" | "medium" | "high";
  reusability_score?: number;
}

export interface Pattern {
  name: string;
  category: string;
  description: string;
  code_example?: string;
  prevalence?: number;
}

export interface LLMStrategy {
  providers: string[];
  streaming: boolean;
  tool_calling: boolean;
  context_optimization: string;
  prompt_engineering?: string;
}

export interface ArchitecturalInsight {
  repo_id: string;
  analyzed_at: string;
  version: string;
  architecture_style: string;
  primary_language: string;
  key_dependencies: string[];
  description?: string;
  components: ComponentAnalysis[];
  llm_strategy: LLMStrategy;
  patterns: Pattern[];
  key_insights: string[];
  analysis_metadata: {
    files_analyzed: number;
    llm_calls: number;
    confidence: number;
    analysis_duration_seconds?: number;
  };
}

export interface CrossPattern {
  pattern_id: string;
  name: string;
  category: string;
  description: string;
  implementations: {
    repo_id: string;
    approach: string;
    maturity?: string;
  }[];
  metadata: {
    prevalence: number;
    maturity: string;
  };
}

export interface ObservatoryData {
  meta: {
    version: string;
    last_updated: string;
    total_repos: number;
  };
  insights: ArchitecturalInsight[];
  patterns: CrossPattern[];
}
