/**
 * Data Loading Abstraction
 *
 * Growth-ready: Easy to swap from static JSON to API
 * Today: Load from static files
 * Tomorrow: Load from API with real-time updates
 */

import { ObservatoryData, ArchitecturalInsight, CrossPattern } from './types';
import observatoryData from '@/public/data/observatory.json';

export interface DataSource {
  loadInsights(): Promise<ArchitecturalInsight[]>;
  loadPatterns(): Promise<CrossPattern[]>;
  getMeta(): Promise<{
    version: string;
    last_updated: string;
    total_repos: number;
  }>;
}

/**
 * Static data source - loads from JSON files
 */
class StaticDataSource implements DataSource {
  private data: ObservatoryData;

  constructor() {
    this.data = observatoryData as ObservatoryData;
  }

  async loadInsights(): Promise<ArchitecturalInsight[]> {
    return this.data.insights || [];
  }

  async loadPatterns(): Promise<CrossPattern[]> {
    return this.data.patterns || [];
  }

  async getMeta() {
    return this.data.meta || {
      version: '1.0',
      last_updated: new Date().toISOString(),
      total_repos: 0
    };
  }

  async getInsightByRepo(repoId: string): Promise<ArchitecturalInsight | null> {
    const insights = await this.loadInsights();
    return insights.find(i => i.repo_id === repoId) || null;
  }
}

/**
 * [Future] Live data source - loads from API
 *
 * Growth hook: When monitoring enabled
 */
class LiveDataSource implements DataSource {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  async loadInsights(): Promise<ArchitecturalInsight[]> {
    const response = await fetch(`${this.baseUrl}/insights`);
    return response.json();
  }

  async loadPatterns(): Promise<CrossPattern[]> {
    const response = await fetch(`${this.baseUrl}/patterns`);
    return response.json();
  }

  async getMeta() {
    const response = await fetch(`${this.baseUrl}/meta`);
    return response.json();
  }
}

// Easy to swap implementations
export const dataSource: DataSource = new StaticDataSource();

// Future: export const dataSource = new LiveDataSource();

// Helper functions
export async function getInsights() {
  return dataSource.loadInsights();
}

export async function getPatterns() {
  return dataSource.loadPatterns();
}

export async function getMeta() {
  return dataSource.getMeta();
}

export async function getInsightByRepo(repoId: string) {
  const insights = await getInsights();
  return insights.find(i => i.repo_id === repoId) || null;
}
