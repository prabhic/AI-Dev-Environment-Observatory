# 🌱 Growth Path Documentation

## How to Evolve the Observatory

This document explains how to evolve each component from its current MVP state to future capabilities.

**Philosophy**: Configuration over code changes. Flip switches, don't rewrite systems.

---

## 1. Repository Registry → Auto-Discovery

### Current State
- 3 hardcoded repositories in `registry/repos.yaml`
- Manual addition of new repos

### Growth Target
- Automatic GitHub scanning for AI-IDE projects
- Daily discovery of new repositories
- Automatic metadata extraction

### Migration Steps

**1. Enable auto-discovery (1 hour)**

```yaml
# steering/config.yaml
experimental:
  auto_discovery: true

discovery:
  enabled: true
  sources:
    - github_topics: ["ai-ide", "ai-coding-assistant"]
    - github_search: "language:TypeScript ai code editor"
  filters:
    min_stars: 1000
    has_activity_last_months: 6
```

**2. Implement discovery logic (3 hours)**

Edit `registry/discovery.py`:

```python
def scan_github(self, topics: List[str], min_stars: int) -> List[Dict]:
    """Scan GitHub for repositories"""
    # Use PyGithub or requests
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    results = []
    for topic in topics:
        url = f"https://api.github.com/search/repositories?q=topic:{topic}+stars:>{min_stars}"
        response = requests.get(url, headers=headers)

        for repo in response.json()["items"]:
            results.append({
                "id": repo["name"].lower(),
                "name": repo["full_name"],
                "url": repo["clone_url"],
                "type": self._infer_type(repo),
                "language": repo["language"],
                "tags": repo["topics"]
            })

    return results
```

**3. Add validation (1 hour)**

```python
def validate_repository(self, repo_url: str) -> bool:
    """Validate repo is suitable for analysis"""
    # Clone repo
    # Check for package.json or pyproject.toml
    # Look for AI/LLM keywords
    # Return True if suitable
```

**4. Schedule discovery (when monitoring enabled)**

```python
# pipeline/scheduler.py
scheduler.schedule_daily(discovery.scan_and_add, hour=2)
```

**Total Effort**: ~4 hours
**Triggers**: When you want to track >10 repos
**Dependencies**: GitHub API token

---

## 2. Analysis Pipeline → Continuous Monitoring

### Current State
- Manual `./run.py analyze` execution
- No change detection
- No scheduled runs

### Growth Target
- Continuous monitoring of repositories
- Triggered updates on repo changes
- Scheduled daily/weekly analysis
- GitHub webhook integration

### Migration Steps

**1. Enable monitoring (immediate)**

```yaml
# steering/config.yaml
monitoring:
  enabled: true
  check_interval_hours: 24
  alert_on_new_patterns: true
  webhook_url: ""  # Optional: Slack/Discord
```

**2. Implement scheduler (4 hours)**

Edit `pipeline/scheduler.py`:

```python
from apscheduler.schedulers.background import BackgroundScheduler

class AnalysisScheduler:
    def __init__(self, config):
        self.scheduler = BackgroundScheduler()
        self.orchestrator = Orchestrator(config)

    def schedule_daily_analysis(self, hour: int = 2):
        """Run full analysis daily"""
        self.scheduler.add_job(
            self.orchestrator.execute,
            trigger='cron',
            hour=hour
        )

    def start_daemon(self):
        self.scheduler.start()
        # Keep alive
        while True:
            time.sleep(60)
```

**3. Add incremental updates (4 hours)**

```python
def update_incremental(self, repo_id: str):
    """Only analyze changed files"""
    # Get last commit from metadata
    # Diff against current
    # Only analyze changed files
    # Merge with existing insights
```

**4. GitHub Webhooks (optional, 4 hours)**

```python
# web/app/api/webhook/route.ts
export async function POST(request: Request) {
    const payload = await request.json()

    if (payload.repository && payload.ref === 'refs/heads/main') {
        // Trigger incremental update
        await triggerAnalysis(payload.repository.name)
    }

    return new Response('OK', { status: 200 })
}
```

**Total Effort**: ~8 hours
**Triggers**: When insights become stale (>1 week old)
**Dependencies**: APScheduler, optional webhook endpoint

---

## 3. Storage → Time-Series Database

### Current State
- JSON files with versioning
- One snapshot per repo
- No historical tracking

### Growth Target
- PostgreSQL + TimescaleDB
- Time-series evolution data
- Queryable insights
- Snapshot comparison

### Migration Steps

**1. Set up PostgreSQL (2 hours)**

```bash
# docker-compose.yml
services:
  postgres:
    image: timescale/timescaledb:latest
    environment:
      POSTGRES_DB: observatory
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

**2. Create schema (2 hours)**

```sql
-- migrations/001_initial.sql
CREATE TABLE repositories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    type TEXT,
    language TEXT,
    metadata JSONB
);

CREATE TABLE insights (
    id SERIAL PRIMARY KEY,
    repo_id TEXT REFERENCES repositories(id),
    analyzed_at TIMESTAMPTZ NOT NULL,
    version TEXT,
    insights JSONB NOT NULL,
    git_commit TEXT
);

-- Make it a hypertable for time-series
SELECT create_hypertable('insights', 'analyzed_at');

CREATE TABLE patterns (
    id SERIAL PRIMARY KEY,
    pattern_id TEXT,
    discovered_at TIMESTAMPTZ,
    pattern_data JSONB
);
```

**3. Implement PostgresStorage (6 hours)**

Edit `storage/storage.py`:

```python
class PostgresStorage(StorageBackend):
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)

    def save_insight(self, repo_id: str, insight: ArchitecturalInsight):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO insights (repo_id, analyzed_at, insights, git_commit)
            VALUES (%s, %s, %s, %s)
        """, (
            repo_id,
            insight.analyzed_at,
            json.dumps(insight.model_dump()),
            self.get_commit(repo_id)
        ))
        self.conn.commit()

    def load_insight(self, repo_id: str) -> ArchitecturalInsight:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT insights FROM insights
            WHERE repo_id = %s
            ORDER BY analyzed_at DESC
            LIMIT 1
        """, (repo_id,))

        row = cursor.fetchone()
        return ArchitecturalInsight(**row[0]) if row else None

    def get_evolution(self, repo_id: str, from_date: str, to_date: str):
        """Get all snapshots in date range"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT analyzed_at, insights FROM insights
            WHERE repo_id = %s
            AND analyzed_at BETWEEN %s AND %s
            ORDER BY analyzed_at
        """, (repo_id, from_date, to_date))

        return [ArchitecturalInsight(**row[1]) for row in cursor.fetchall()]
```

**4. Update config (immediate)**

```yaml
# steering/config.yaml
storage:
  format: "postgres"
  postgres_connection: "postgresql://user:pass@localhost:5432/observatory"
```

**5. Migration script (2 hours)**

```python
# scripts/migrate_to_postgres.py
def migrate():
    json_storage = JSONStorage()
    postgres_storage = PostgresStorage(config["postgres_connection"])

    # Migrate all insights
    for insight in json_storage.load_all_insights():
        postgres_storage.save_insight(insight.repo_id, insight)

    # Migrate patterns
    patterns = json_storage.load_patterns()
    postgres_storage.save_patterns(patterns)
```

**Total Effort**: ~12 hours
**Triggers**: When you need evolution tracking or >50 repos
**Dependencies**: PostgreSQL, TimescaleDB, psycopg2

---

## 4. Intelligence → Multi-Agent System

### Current State
- Single LLM call for synthesis
- One-size-fits-all prompts
- No specialized agents

### Growth Target
- Multiple specialized agents
- Collaborative analysis
- Fine-tuned models for specific tasks
- Confidence scoring

### Migration Steps

**1. Design agent architecture (2 hours)**

```python
# intelligence/agents/base.py
class Agent(ABC):
    @abstractmethod
    def analyze(self, data: Dict) -> Dict:
        pass

# intelligence/agents/architectural_agent.py
class ArchitecturalAgent(Agent):
    """Specialized in architectural patterns"""
    def analyze(self, data: Dict) -> Dict:
        prompt = self.load_prompt("architectural_analysis")
        # LLM call focused on architecture
        return insights

# intelligence/agents/pattern_agent.py
class PatternAgent(Agent):
    """Specialized in pattern detection"""
    def analyze(self, data: Dict) -> Dict:
        # Use smaller, faster model
        # Focus on pattern matching
        return patterns

# intelligence/agents/evolution_agent.py
class EvolutionAgent(Agent):
    """Specialized in tracking changes"""
    def analyze(self, current: Dict, previous: Dict) -> Dict:
        # Compare snapshots
        # Identify changes
        return evolution_insights
```

**2. Implement orchestration (4 hours)**

```python
class MultiAgentIntelligence:
    def __init__(self, config):
        self.agents = {
            "architectural": ArchitecturalAgent(config),
            "pattern": PatternAgent(config),
            "evolution": EvolutionAgent(config),
            "llm_integration": LLMIntegrationAgent(config)
        }

    def synthesize_insights(self, repo_data, analysis):
        results = {}

        # Run agents in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                name: executor.submit(agent.analyze, analysis)
                for name, agent in self.agents.items()
            }

            for name, future in futures.items():
                results[name] = future.result()

        # Merge results
        return self._merge_insights(results)
```

**3. Add ML-based pattern detection (8 hours)**

```python
class MLPatternDetector:
    """Use trained models for pattern detection"""

    def __init__(self):
        self.model = self.load_model()

    def detect_patterns(self, code: str) -> List[Pattern]:
        # Use trained model (e.g., CodeBERT)
        embeddings = self.model.encode(code)
        patterns = self.classify_patterns(embeddings)
        return patterns
```

**4. Enable in config (immediate)**

```yaml
# steering/config.yaml
intelligence:
  mode: "multi_agent"  # single | multi_agent
  agents:
    - architectural
    - pattern
    - evolution
    - llm_integration

experimental:
  ml_pattern_detection: true
```

**Total Effort**: ~16 hours
**Triggers**: When analysis quality plateaus or speed is needed
**Dependencies**: Concurrent execution, optional ML models

---

## 5. Web UI → Real-Time Dashboard

### Current State
- Static Next.js export
- Data loaded from JSON files
- Manual refresh needed

### Growth Target
- Real-time updates via WebSocket
- Live monitoring dashboard
- API endpoints for external tools
- Interactive filters and search

### Migration Steps

**1. Add API routes (4 hours)**

```typescript
// web/app/api/insights/route.ts
export async function GET() {
  const storage = new StorageLayer(config)
  const insights = await storage.load_all_insights()
  return Response.json(insights)
}

// web/app/api/insights/[repo]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { repo: string } }
) {
  const storage = new StorageLayer(config)
  const insight = await storage.load_insight(params.repo)
  return Response.json(insight)
}
```

**2. Switch to LiveDataSource (1 hour)**

```typescript
// web/lib/data-loader.ts
export const dataSource = new LiveDataSource('/api')
```

**3. Add WebSocket support (4 hours)**

```typescript
// web/lib/websocket.ts
const ws = new WebSocket('ws://localhost:8000/ws')

ws.onmessage = (event) => {
  const update = JSON.parse(event.data)

  if (update.type === 'insight_updated') {
    // Refresh data
    mutate('/api/insights')
  }
}
```

**4. Real-time components (4 hours)**

```typescript
'use client'

export function LiveMonitor() {
  const { data, error } = useSWR('/api/status', {
    refreshInterval: 5000  // Poll every 5s
  })

  return (
    <div>
      <h3>Live Status</h3>
      <p>Active analyses: {data?.active}</p>
      <p>Queue: {data?.queued}</p>
    </div>
  )
}
```

**5. Enable in config (immediate)**

```yaml
# steering/config.yaml
web:
  mode: "dynamic"
  enable_api: true
  enable_websocket: true
```

**Total Effort**: ~10 hours
**Triggers**: When monitoring is enabled
**Dependencies**: SWR for React, WebSocket server

---

## 6. Community → Open Research Platform

### Current State
- Solo-maintained
- No user accounts
- No contributions

### Growth Target
- User authentication
- Community-submitted repositories
- Voting on insights
- Research paper generator
- API for researchers

### Migration Steps

**1. Add authentication (8 hours)**

```typescript
// Using Next-Auth
import NextAuth from 'next-auth'
import GithubProvider from 'next-auth/providers/github'

export const authOptions = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
  ],
}
```

**2. Community submissions (6 hours)**

```typescript
// web/app/api/submit/route.ts
export async function POST(request: Request) {
  const session = await getServerSession()
  if (!session) return new Response('Unauthorized', { status: 401 })

  const { repoUrl } = await request.json()

  // Validate repository
  // Add to pending queue
  // Notify moderators

  return Response.json({ status: 'pending' })
}
```

**3. Voting system (6 hours)**

```sql
CREATE TABLE votes (
    user_id TEXT,
    insight_id INT REFERENCES insights(id),
    vote INT CHECK (vote IN (-1, 1)),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, insight_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    insight_id INT REFERENCES insights(id),
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**4. Research paper generator (12 hours)**

```python
# intelligence/research.py
class ResearchPaperGenerator:
    def generate_paper(self, topic: str) -> str:
        """Generate LaTeX research paper"""

        insights = self.storage.load_all_insights()

        # Aggregate data
        patterns = self._aggregate_patterns(insights)
        trends = self._identify_trends(insights)

        # Use LLM to write sections
        abstract = self._generate_abstract(patterns, trends)
        introduction = self._generate_intro()
        methods = self._describe_methods()
        results = self._present_results(patterns)
        discussion = self._generate_discussion(trends)

        # Compile LaTeX
        return self._compile_latex(
            abstract, introduction, methods, results, discussion
        )
```

**5. Public API (4 hours)**

```python
# api/main.py (FastAPI)
@app.get("/api/v1/insights")
async def get_insights(
    skip: int = 0,
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    insights = storage.load_all_insights()
    return insights[skip:skip+limit]

@app.get("/api/v1/patterns")
async def get_patterns():
    return storage.load_patterns()

@app.get("/api/v1/evolution/{repo_id}")
async def get_evolution(repo_id: str, from_date: str, to_date: str):
    return storage.get_evolution(repo_id, from_date, to_date)
```

**6. Enable in config (immediate)**

```yaml
# steering/config.yaml
experimental:
  community_contributions: true
  voting_enabled: true
  api_enabled: true

community:
  require_approval: true
  moderators: ["user1", "user2"]
```

**Total Effort**: ~40 hours
**Triggers**: When external interest grows
**Dependencies**: Auth system, moderation tools

---

## Feature Priority Matrix

| Feature | Effort | Impact | Priority | Triggers |
|---------|--------|--------|----------|----------|
| Auto-Discovery | 4h | High | 🟢 High | >10 repos wanted |
| Monitoring | 8h | High | 🟢 High | Insights stale |
| Time-Series DB | 12h | Medium | 🟡 Medium | Evolution tracking needed |
| Multi-Agent | 16h | Medium | 🟡 Medium | Quality/speed plateau |
| Real-Time UI | 10h | Low | 🔴 Low | Monitoring enabled |
| Community | 40h | Low | 🔴 Low | External interest |

## Quick Wins (< 4 hours each)

1. **Add more repositories** - Edit YAML (30 min)
2. **Improve prompts** - Refine prompt templates (2 hours)
3. **Better UI** - Enhance components (3 hours)
4. **Export formats** - Add CSV/PDF export (2 hours)
5. **Search/Filter** - Add UI search (3 hours)

## Configuration Reference

All growth features have config switches:

```yaml
# steering/config.yaml

# Feature switches
experimental:
  auto_discovery: false       # → Auto-discover repos
  monitoring: false           # → Continuous updates
  ml_pattern_detection: false # → ML-based patterns
  github_webhooks: false      # → Webhook triggers
  community_contributions: false  # → Open platform

# Phase 2 config
monitoring:
  enabled: false
  check_interval_hours: 24
  alert_on_new_patterns: false

# Phase 3 config
storage:
  format: "json"  # → "postgres" for time-series
  versioning: true

# Phase 4 config
intelligence:
  mode: "single"  # → "multi_agent"
  agents: ["architectural", "pattern", "evolution"]

# Phase 5 config
web:
  mode: "static"  # → "dynamic"
  enable_api: false
  enable_websocket: false

# Phase 6 config
community:
  enabled: false
  require_approval: true
  voting_enabled: false
```

## Migration Checklist

When growing a feature:

- [ ] Read this growth path section
- [ ] Estimate effort and dependencies
- [ ] Update configuration
- [ ] Implement core functionality
- [ ] Test thoroughly
- [ ] Update documentation
- [ ] Commit changes
- [ ] Monitor for issues

---

**Remember**: This is a seed architecture. Growth is meant to be easy!
