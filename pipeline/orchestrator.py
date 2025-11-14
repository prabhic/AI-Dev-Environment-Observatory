"""
Analysis Orchestrator

Coordinates the entire analysis pipeline.

Growth hooks:
- Today: Sequential analysis of repos
- Phase 2: Parallel analysis with job queue
- Phase 3: Incremental updates (only changed files)
- Phase 4: Real-time monitoring with webhooks
"""

import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from registry.registry import RepositoryRegistry
from analyzers.core.git_ops import GitOperations
from analyzers.core.file_scanner import FileScanner
from analyzers.architectural.component_analyzer import ComponentAnalyzer
from analyzers.architectural.pattern_extractor import PatternExtractor
from analyzers.architectural.llm_integration_analyzer import LLMIntegrationAnalyzer
from intelligence.agent import IntelligenceAgent
from storage.storage import StorageLayer
from intelligence.models import AnalysisRun

console = Console()


class Orchestrator:
    """
    Self-driving analysis coordinator

    Growth path:
    - Today: Sequential analysis of 3 repos
    - Phase 2: Parallel analysis with job queue
    - Phase 3: Incremental updates (only changed files)
    - Phase 4: Real-time monitoring with webhooks
    """

    def __init__(self, config: Dict):
        self.config = config

        # Initialize components
        console.print("[bold blue]🚀 Initializing AI-IDE Observatory[/bold blue]\n")

        self.registry = RepositoryRegistry(config["registry"]["source"])
        self.git_ops = GitOperations()
        self.file_scanner = FileScanner(
            max_file_size_kb=config["analysis"]["file_size_limit_kb"]
        )

        # Initialize analyzers
        self.analyzers = {
            "components": ComponentAnalyzer(config["analysis"]),
            "patterns": PatternExtractor(config["analysis"]),
            "llm_integration": LLMIntegrationAnalyzer(config["analysis"])
        }

        # Initialize intelligence layer
        self.intelligence = IntelligenceAgent(config["intelligence"])

        # Initialize storage
        self.storage = StorageLayer(config["storage"])

        # Track run metadata
        self.run = AnalysisRun(
            run_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            started_at=datetime.now()
        )

    def execute(self, repo_filter: str = None) -> None:
        """
        Main execution pipeline

        Args:
            repo_filter: Optional repository ID to analyze (otherwise all)
        """
        console.print(
            "[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]"
        )
        console.print("[bold cyan]  ANALYSIS PIPELINE STARTING[/bold cyan]")
        console.print(
            "[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n"
        )

        # Get repositories to analyze
        if repo_filter:
            repo = self.registry.get_repository(repo_filter)
            repos = [repo] if repo else []
            if not repos:
                console.print(f"[red]✗[/red] Repository not found: {repo_filter}")
                return
        else:
            repos = self.registry.get_active_repos()

        self.run.total_repos = len(repos)
        console.print(f"[cyan]📊[/cyan] Analyzing {len(repos)} repositories\n")

        # Analyze each repository
        for i, repo in enumerate(repos, 1):
            console.print(
                f"\n[bold yellow]{'═' * 60}[/bold yellow]"
            )
            console.print(
                f"[bold yellow] [{i}/{len(repos)}] {repo.name}[/bold yellow]"
            )
            console.print(
                f"[bold yellow]{'═' * 60}[/bold yellow]\n"
            )

            try:
                self._analyze_repository(repo)
                self.run.successful += 1
                self.run.repos_analyzed.append(repo.id)
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to analyze {repo.name}: {e}")
                self.run.failed += 1
                self.run.errors.append(f"{repo.id}: {str(e)}")

        # Cross-repository pattern analysis
        console.print(
            f"\n[bold magenta]{'═' * 60}[/bold magenta]"
        )
        console.print("[bold magenta] CROSS-REPOSITORY ANALYSIS[/bold magenta]")
        console.print(
            f"[bold magenta]{'═' * 60}[/bold magenta]\n"
        )

        self._cross_analysis()

        # Finalize
        self.run.completed_at = datetime.now()
        self.storage.save_run_metadata(self.run)

        # Export for web UI
        console.print(f"\n[bold green]{'═' * 60}[/bold green]")
        console.print("[bold green] EXPORTING DATA[/bold green]")
        console.print(f"[bold green]{'═' * 60}[/bold green]\n")

        self.export_for_web()

        # Summary
        self._print_summary()

    def _analyze_repository(self, repo) -> None:
        """Analyze a single repository"""
        start_time = time.time()

        # 1. Clone/update repository
        repo_path = self.git_ops.clone_or_update(repo.url, repo.id)

        # 2. Scan files
        file_data = self.file_scanner.scan_repository(
            repo_path,
            max_files=self.config["analysis"]["max_files_per_repo"]
        )

        # 3. Run all analyzers
        console.print(f"[cyan]🔬[/cyan] Running analyzers...")
        analysis_results = {}

        for analyzer_name, analyzer in self.analyzers.items():
            if analyzer.should_run(repo):
                try:
                    results = analyzer.analyze(repo_path, file_data)
                    analysis_results[analyzer_name] = results
                except Exception as e:
                    console.print(
                        f"[yellow]⚠[/yellow] {analyzer.get_name()} failed: {e}"
                    )

        # 4. Generate insights via LLM
        repo_data = repo.model_dump()
        insights = self.intelligence.synthesize_insights(repo_data, analysis_results)

        # 5. Store insights
        self.storage.save_insights(repo.id, insights)

        elapsed = time.time() - start_time
        console.print(f"[green]✓[/green] Completed in {elapsed:.1f}s")

    def _cross_analysis(self) -> None:
        """Perform cross-repository pattern analysis"""
        all_insights = self.storage.get_all_insights()

        if len(all_insights) < 2:
            console.print(
                "[yellow]⚠[/yellow] Need at least 2 repos for cross-analysis"
            )
            return

        # Extract cross-patterns
        patterns = self.intelligence.extract_cross_patterns(all_insights)

        # Store patterns
        self.storage.save_patterns(patterns)

    def export_for_web(self) -> None:
        """Export data for web UI"""
        self.storage.export_for_web()

        # Also export registry
        registry_data = self.registry.export_for_web()
        registry_path = Path("web/public/data/registry.json")
        registry_path.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)

        console.print("[green]✓[/green] Exported registry for web UI")

    def _print_summary(self) -> None:
        """Print analysis summary"""
        duration = (self.run.completed_at - self.run.started_at).total_seconds()

        console.print(f"\n\n[bold green]{'━' * 60}[/bold green]")
        console.print("[bold green] ANALYSIS COMPLETE[/bold green]")
        console.print(f"[bold green]{'━' * 60}[/bold green]\n")

        console.print(f"[cyan]Total repositories:[/cyan] {self.run.total_repos}")
        console.print(f"[green]Successful:[/green] {self.run.successful}")
        console.print(f"[red]Failed:[/red] {self.run.failed}")
        console.print(f"[cyan]Duration:[/cyan] {duration:.1f}s")

        if self.run.errors:
            console.print(f"\n[yellow]Errors:[/yellow]")
            for error in self.run.errors:
                console.print(f"  - {error}")

        console.print(f"\n[cyan]💡 Next steps:[/cyan]")
        console.print("  1. cd web && npm install && npm run dev")
        console.print("  2. Open http://localhost:3000")
        console.print("  3. Explore insights and patterns!")

    # [Future] Methods for growth

    def monitor(self) -> None:
        """
        [Future] Start continuous monitoring

        Growth hook: When monitoring enabled in config
        """
        raise NotImplementedError("Continuous monitoring not yet enabled")

    def update_incremental(self, repo_id: str) -> None:
        """
        [Future] Incremental update (only analyze changed files)

        Growth hook: For efficiency at scale
        """
        raise NotImplementedError("Incremental updates not yet enabled")

    def analyze_parallel(self, repos: list) -> None:
        """
        [Future] Parallel analysis using job queue

        Growth hook: When analyzing >10 repos
        """
        raise NotImplementedError("Parallel analysis not yet enabled")
