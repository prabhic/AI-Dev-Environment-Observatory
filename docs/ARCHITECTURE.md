# 🏗️ Architecture Documentation

## Overview

The AI-IDE Observatory is built on a **seed architecture** - minimal now, but designed to grow into a comprehensive research platform with minimal refactoring.

## Core Principles

### 1. Layered Architecture

```
┌─────────────────────────────────────┐
│  Steering Layer (config.yaml)      │  ← Configuration-driven control
├─────────────────────────────────────┤
│  Orchestration (pipeline/)          │  ← Coordinates all components
├─────────────────────────────────────┤
│  Intelligence (intelligence/)       │  ← LLM-powered insights
├─────────────────────────────────────┤
│  Analysis (analyzers/)              │  ← Pluggable analyzers
├─────────────────────────────────────┤
│  Storage (storage/)                 │  ← Abstracted persistence
├─────────────────────────────────────┤
│  Presentation (web/)                │  ← User interface
└─────────────────────────────────────┘
```

### 2. Growth-Ready Design

Every component has:
- **Abstraction boundaries** - Easy to swap implementations
- **Configuration hooks** - Behavior controlled by config
- **Future stubs** - Methods for upcoming features
- **Versioning** - Data schemas support evolution

### 3. Configuration Over Code

```yaml
# Flip switches, don't rewrite code
monitoring:
  enabled: false  # Change to true → system adapts
```

## Component Details

### Registry System (`registry/`)

**Purpose**: Manages repository metadata and discovery

**Key Files**:
- `repos.yaml` - Source of truth for tracked repos
- `registry.py` - Registry management
- `models.py` - Pydantic models for type safety
- `discovery.py` - [Future] Auto-discovery

**Growth Path**:
- Today: YAML file with 3 repos
- Tomorrow: Database with auto-discovery
- Future: Community submissions

**Interfaces**:
```python
class RepositoryRegistry:
    def get_all_repositories() -> List[Repository]
    def get_repository(repo_id: str) -> Repository
    def get_active_repos() -> List[Repository]  # Growth hook
```

### Analysis Engine (`analyzers/`)

**Purpose**: Extract structural and architectural information

**Structure**:
```
analyzers/
├── core/
│   ├── base_analyzer.py      # Abstract base
│   ├── git_ops.py             # Git operations
│   └── file_scanner.py        # Smart file detection
├── architectural/
│   ├── component_analyzer.py
│   ├── pattern_extractor.py
│   └── llm_integration_analyzer.py
└── evolutionary/              # [Future]
    └── diff_analyzer.py
```

**Pluggable Design**:
```python
class BaseAnalyzer(ABC):
    def analyze(self, repo_path: Path, file_data: Dict) -> Dict
    def should_run(self, repo: Repository) -> bool  # Growth hook
```

New analyzers can be added without changing the orchestrator.

**Key Analyzers**:

1. **ComponentAnalyzer**
   - Identifies architectural components
   - Categorizes files (entry point, LLM integration, UI, etc.)
   - Estimates complexity

2. **PatternExtractor**
   - Detects coding patterns (async, streaming, etc.)
   - Extracts code examples
   - Categorizes patterns

3. **LLMIntegrationAnalyzer**
   - Identifies LLM providers
   - Detects streaming, tool calling
   - Finds context optimization strategies

### Intelligence Layer (`intelligence/`)

**Purpose**: LLM-powered insight synthesis

**Structure**:
```
intelligence/
├── agent.py           # LLM orchestration
├── models.py          # Pydantic schemas
├── prompts/           # Versioned prompts
│   ├── v1_architectural.txt
│   └── v1_cross_analysis.txt
└── cache.py           # [Future] Caching layer
```

**Key Classes**:

```python
class IntelligenceAgent:
    def synthesize_insights(
        self, repo_data: Dict, analysis: Dict
    ) -> ArchitecturalInsight

    def extract_cross_patterns(
        self, all_insights: List
    ) -> List[CrossPattern]
```

**Data Models** (Pydantic):
- `ArchitecturalInsight` - Complete repo analysis
- `ComponentAnalysis` - Single component
- `Pattern` - Code/architectural pattern
- `CrossPatternInsight` - Multi-repo pattern
- `LLMStrategy` - LLM integration details

**Growth Hooks**:
- Today: Single LLM call for synthesis
- Phase 2: Multi-agent system (specialized agents)
- Phase 3: Fine-tuned models for patterns

### Storage Layer (`storage/`)

**Purpose**: Versioned, abstracted data persistence

**Design Pattern**: Strategy pattern for easy backend swapping

```python
class StorageBackend(ABC):
    def save_insight(repo_id, insight) -> None
    def load_insight(repo_id) -> ArchitecturalInsight
    # ...

class JSONStorage(StorageBackend):  # Current
class PostgresStorage(StorageBackend):  # Future
```

**Data Structure**:
```
storage/
├── schema/
│   ├── insight_v1.json
│   └── pattern_v1.json
├── insights/
│   └── v1/
│       ├── cline/insights.json
│       ├── continue/insights.json
│       └── metadata.json
└── patterns/
    └── v1_patterns.json
```

**Growth Path**:
- Today: JSON files with versioning
- Phase 2: SQLite for queryability
- Phase 3: PostgreSQL + TimescaleDB for time-series

**Versioning Strategy**:
- All schemas include `version` field
- New versions coexist with old ones
- Automatic migration on schema changes

### Pipeline Orchestrator (`pipeline/`)

**Purpose**: Coordinates the entire analysis workflow

**Main Flow**:

```python
def execute(repo_filter=None):
    # 1. Get repositories from registry
    repos = registry.get_active_repos()

    for repo in repos:
        # 2. Clone/update repository
        repo_path = git_ops.clone_or_update(repo.url, repo.id)

        # 3. Scan files intelligently
        file_data = file_scanner.scan_repository(repo_path)

        # 4. Run all analyzers
        for analyzer in analyzers:
            results[analyzer.name] = analyzer.analyze(repo_path, file_data)

        # 5. Synthesize with LLM
        insights = intelligence.synthesize_insights(repo, results)

        # 6. Store versioned insights
        storage.save_insights(repo.id, insights)

    # 7. Cross-repository analysis
    patterns = intelligence.extract_cross_patterns(all_insights)
    storage.save_patterns(patterns)

    # 8. Export for web UI
    storage.export_for_web()
```

**Growth Hooks**:
```python
def monitor():  # [Future] Continuous monitoring
def analyze_parallel(repos):  # [Future] Parallel processing
def update_incremental(repo_id):  # [Future] Incremental updates
```

### Web UI (`web/`)

**Tech Stack**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Static export (no server needed)

**Structure**:
```
web/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Dashboard
│   ├── repos/[slug]/       # Repo detail pages
│   └── patterns/           # Pattern explorer
├── components/
│   └── InsightCard.tsx
├── lib/
│   ├── types.ts            # TypeScript types
│   └── data-loader.ts      # Abstracted data loading
└── public/
    └── data/
        └── observatory.json
```

**Data Loading Abstraction**:

```typescript
interface DataSource {
  loadInsights(): Promise<ArchitecturalInsight[]>
  loadPatterns(): Promise<CrossPattern[]>
}

class StaticDataSource implements DataSource {
  // Loads from JSON files
}

class LiveDataSource implements DataSource {
  // [Future] Loads from API with real-time updates
}

// Easy to swap!
export const dataSource: DataSource = new StaticDataSource()
```

**Growth Path**:
- Today: Static Next.js export
- Phase 2: API routes for dynamic data
- Phase 3: WebSocket for real-time updates
- Phase 4: Authentication and community features

## Data Flow

```
┌─────────────┐
│   GitHub    │
│ Repositories│
└──────┬──────┘
       │ git clone
       ▼
┌─────────────┐
│  File       │
│  Scanner    │
└──────┬──────┘
       │ files + metadata
       ▼
┌─────────────┐
│  Analyzers  │ (component, pattern, LLM integration)
└──────┬──────┘
       │ raw analysis
       ▼
┌─────────────┐
│Intelligence │
│   Layer     │ (LLM synthesis)
└──────┬──────┘
       │ insights
       ▼
┌─────────────┐
│  Storage    │ (versioned JSON)
└──────┬──────┘
       │ export
       ▼
┌─────────────┐
│   Web UI    │ (Next.js dashboard)
└─────────────┘
```

## Configuration System

All behavior controlled via `steering/config.yaml`:

```yaml
analysis:
  mode: "full"              # full | incremental | targeted
  llm_provider: "anthropic"
  max_files_per_repo: 100

intelligence:
  prompt_version: "v1"
  enable_pattern_detection: true
  enable_evolution_tracking: false  # Growth switch

storage:
  format: "json"            # json | sqlite | postgres
  versioning: true

experimental:
  auto_discovery: false     # GitHub scanning
  monitoring: false         # Continuous updates
```

**No code changes needed** - just flip switches!

## Extensibility Points

### Adding New Repositories

1. Edit `registry/repos.yaml`
2. Run `steer_analyze`

### Adding New Analyzers

```python
class CustomAnalyzer(BaseAnalyzer):
    def get_name(self) -> str:
        return "CustomAnalyzer"

    def analyze(self, repo_path, file_data) -> Dict:
        # Your analysis logic
        return results

# Register in orchestrator
orchestrator.analyzers["custom"] = CustomAnalyzer(config)
```

### Adding New Storage Backend

```python
class NewStorage(StorageBackend):
    def save_insight(self, repo_id, insight):
        # Your storage logic
        pass

# Configure in config.yaml
storage:
  format: "newstorage"
```

### Adding New Data Sources (Web UI)

```typescript
class APIDataSource implements DataSource {
  async loadInsights() {
    return fetch('/api/insights').then(r => r.json())
  }
}

export const dataSource = new APIDataSource()
```

## Error Handling

- **Git Operations**: Continue with cached version on pull failure
- **Analysis**: Skip failed analyzers, continue pipeline
- **LLM Calls**: Fallback to basic insights if LLM unavailable
- **Storage**: Validate schemas before writing

## Performance Considerations

**Current (MVP)**:
- Sequential analysis (good for 3-10 repos)
- Shallow git clones (faster)
- File size limits (skip large files)
- LLM call caching (future)

**Future Optimizations**:
- Parallel repository analysis
- Incremental updates (only changed files)
- ML-based pattern detection (faster than LLM)
- Database indexing for queries

## Security

- No sensitive data stored
- API keys via environment variables
- Gitignore for cloned repos
- Static site export (no server vulnerabilities)

## Testing Strategy

**Current**:
- Type safety via Pydantic and TypeScript
- Schema validation
- Manual integration testing

**Future**:
- Unit tests for analyzers
- Integration tests for pipeline
- E2E tests for web UI
- Regression tests for insights quality

## Deployment

**Current**:
- Run locally: `python run.py analyze && python run.py serve`
- Deploy web UI: `cd web && npm run build` → Deploy to Vercel/Netlify

**Future**:
- Docker containers
- GitHub Actions for CI/CD
- Scheduled analysis runs
- API deployment

## Monitoring & Observability

**Future Additions**:
- Analysis run metadata (already stored)
- LLM call tracking
- Performance metrics
- Error reporting
- Health checks

---

See [GROWTH_PATH.md](GROWTH_PATH.md) for how to evolve each component.
