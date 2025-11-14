#!/usr/bin/env python3
"""
AI-IDE Observatory - Self-Driving Orchestrator

Usage:
  ./run.py analyze              # Run full analysis
  ./run.py analyze --repo cline # Analyze single repo
  ./run.py serve                # Start web UI locally
  ./run.py export               # Export data for web

[Future Commands - Already Stubbed]
  ./run.py monitor              # Start continuous monitoring
  ./run.py discover             # Find new AI-IDEs
"""

import sys
import yaml
import click
from pathlib import Path
from rich.console import Console

from pipeline.orchestrator import Orchestrator
from steering.config import load_config

console = Console()


@click.group()
def cli():
    """AI-IDE Observatory - Self-Evolving Research Platform"""
    pass


@cli.command()
@click.option('--repo', default=None, help='Analyze specific repository (optional)')
def analyze(repo):
    """Run analysis pipeline"""
    console.print("\n[bold blue]🔬 AI-IDE Observatory[/bold blue]")
    console.print("[dim]Self-Evolving Research Platform[/dim]\n")

    # Load configuration
    config = load_config()

    # Initialize and run orchestrator
    orchestrator = Orchestrator(config)
    orchestrator.execute(repo_filter=repo)


@cli.command()
def serve():
    """Start web UI development server"""
    import subprocess
    import os

    web_dir = Path("web")

    if not web_dir.exists():
        console.print("[red]✗[/red] Web directory not found. Run 'analyze' first.")
        return

    console.print("[cyan]🌐[/cyan] Starting web UI...")
    console.print("[dim]Navigate to: http://localhost:3000[/dim]\n")

    # Check if node_modules exists
    if not (web_dir / "node_modules").exists():
        console.print("[yellow]⚠[/yellow] Installing dependencies...")
        subprocess.run(["npm", "install"], cwd=web_dir)

    # Start dev server
    subprocess.run(["npm", "run", "dev"], cwd=web_dir)


@cli.command()
def export():
    """Export data for web UI"""
    config = load_config()

    from storage.storage import StorageLayer
    from registry.registry import RepositoryRegistry

    storage = StorageLayer(config["storage"])
    registry = RepositoryRegistry(config["registry"]["source"])

    console.print("[cyan]📦[/cyan] Exporting data for web UI...")

    # Export insights and patterns
    storage.export_for_web()

    # Export registry
    import json
    registry_path = Path("web/public/data/registry.json")
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    with open(registry_path, 'w') as f:
        json.dump(registry.export_for_web(), f, indent=2)

    console.print("[green]✓[/green] Export complete")


@cli.command()
def monitor():
    """
    [Future] Start continuous monitoring

    Not yet enabled. Edit steering/config.yaml to enable:
      monitoring.enabled = true
    """
    console.print("[yellow]⚠[/yellow] Continuous monitoring not yet enabled")
    console.print("Edit steering/config.yaml and set monitoring.enabled = true")
    console.print("\nGrowth path documentation: docs/GROWTH_PATH.md")


@cli.command()
def discover():
    """
    [Future] Discover new AI-IDE repositories

    Not yet enabled. Edit steering/config.yaml to enable:
      experimental.auto_discovery = true
    """
    console.print("[yellow]⚠[/yellow] Auto-discovery not yet enabled")
    console.print("Edit steering/config.yaml and set experimental.auto_discovery = true")
    console.print("\nGrowth path documentation: docs/GROWTH_PATH.md")


def main():
    """Entry point"""
    cli()


if __name__ == "__main__":
    main()
