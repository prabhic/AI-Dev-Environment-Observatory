"""
Git Operations

Handles cloning and updating repositories.

Growth hooks:
- clone_or_update() -> Can add shallow clones for speed
- get_commit_history() -> For evolution tracking
"""

import git
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()


class GitOperations:
    """
    Manages Git operations for repository analysis

    Growth-ready:
    - Today: Simple clone/pull
    - Phase 2: Shallow clones, specific branches
    - Phase 3: Commit history analysis for evolution tracking
    """

    def __init__(self, storage_path: str = "storage/repos"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def clone_or_update(self, repo_url: str, repo_id: str) -> Path:
        """
        Clone repository or update if already exists

        Args:
            repo_url: Git clone URL
            repo_id: Repository identifier (for local path)

        Returns:
            Path to local repository
        """
        repo_path = self.storage_path / repo_id

        if repo_path.exists():
            console.print(f"[yellow]↻[/yellow] Updating {repo_id}...")
            try:
                repo = git.Repo(repo_path)
                origin = repo.remotes.origin
                origin.pull()
                console.print(f"[green]✓[/green] Updated {repo_id}")
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to update {repo_id}: {e}")
                # Continue with existing version
        else:
            console.print(f"[blue]↓[/blue] Cloning {repo_id}...")
            try:
                git.Repo.clone_from(repo_url, repo_path, depth=1)  # Shallow clone for speed
                console.print(f"[green]✓[/green] Cloned {repo_id}")
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to clone {repo_id}: {e}")
                raise

        return repo_path

    def get_latest_commit(self, repo_path: Path) -> Optional[str]:
        """Get latest commit hash"""
        try:
            repo = git.Repo(repo_path)
            return repo.head.commit.hexsha
        except:
            return None

    def get_commit_date(self, repo_path: Path) -> Optional[str]:
        """Get latest commit date"""
        try:
            repo = git.Repo(repo_path)
            return repo.head.commit.committed_datetime.isoformat()
        except:
            return None

    def get_commit_history(self, repo_path: Path, since: Optional[str] = None) -> list:
        """
        [Future] Get commit history for evolution tracking

        Args:
            repo_path: Path to repository
            since: ISO date string to get commits since

        Returns:
            List of commits with metadata
        """
        raise NotImplementedError("Commit history analysis not yet enabled")

    def checkout_commit(self, repo_path: Path, commit_hash: str) -> None:
        """
        [Future] Checkout specific commit for time-series analysis
        """
        raise NotImplementedError("Commit checkout not yet enabled")
