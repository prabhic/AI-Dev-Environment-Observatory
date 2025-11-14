"""
Repository Registry

Manages the repository registry, loading and validating repos.yaml.

Growth hooks:
- load_repositories() -> Can be extended to load from database
- validate_repository() -> Can add more sophisticated validation
- get_active_repos() -> Can filter by health status when monitoring enabled
"""

import yaml
from pathlib import Path
from typing import List, Optional, Dict
from rich.console import Console

from registry.models import Repository, RegistrySchema

console = Console()


class RepositoryRegistry:
    """
    Manages repository registry

    Today: Loads from YAML file
    Tomorrow: Can integrate with database, auto-discovery, monitoring
    """

    def __init__(self, registry_path: str = "registry/repos.yaml"):
        self.registry_path = Path(registry_path)
        self.schema: Optional[RegistrySchema] = None
        self.repositories: List[Repository] = []
        self._load()

    def _load(self) -> None:
        """Load and validate registry from YAML"""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        with open(self.registry_path, 'r') as f:
            data = yaml.safe_load(f)

        # Validate against schema
        self.schema = RegistrySchema(**data)
        self.repositories = self.schema.repositories

        console.print(
            f"[green]✓[/green] Loaded {len(self.repositories)} repositories from registry"
        )

    def get_all_repositories(self) -> List[Repository]:
        """Get all registered repositories"""
        return self.repositories

    def get_repository(self, repo_id: str) -> Optional[Repository]:
        """Get a specific repository by ID"""
        for repo in self.repositories:
            if repo.id == repo_id:
                return repo
        return None

    def get_active_repos(self) -> List[Repository]:
        """
        Get repositories that should be analyzed

        Growth hook: When monitoring enabled, filter by health_status
        """
        # Today: Return all repos
        # Tomorrow: Filter by health_status != "archived"
        return self.repositories

    def get_by_priority(self, priority: str) -> List[Repository]:
        """Get repositories by analysis priority"""
        return [r for r in self.repositories if r.analysis_priority == priority]

    def get_by_type(self, repo_type: str) -> List[Repository]:
        """Get repositories by type"""
        return [r for r in self.repositories if r.type == repo_type]

    def get_by_tag(self, tag: str) -> List[Repository]:
        """Get repositories by tag"""
        return [r for r in self.repositories if tag in r.tags]

    def validate_repository(self, repo: Repository) -> bool:
        """
        Validate repository entry

        Growth hook: Can add more validation:
        - Check if URL is accessible
        - Verify repository exists on GitHub
        - Check minimum stars/activity
        """
        # Basic validation via Pydantic models
        return True

    def add_repository(self, repo: Repository) -> None:
        """
        [Future] Add a new repository to the registry

        Growth hook: When auto-discovery enabled
        """
        raise NotImplementedError("Manual repository addition not yet implemented")

    def update_repository_status(self, repo_id: str, status: Dict) -> None:
        """
        [Future] Update repository metadata (last_analyzed, health_status)

        Growth hook: When monitoring enabled
        """
        raise NotImplementedError("Status updates not yet implemented")

    def export_for_web(self) -> Dict:
        """Export registry in format suitable for web UI"""
        return {
            "version": self.schema.version,
            "last_updated": self.schema.last_updated,
            "total_repos": len(self.repositories),
            "repositories": [repo.model_dump() for repo in self.repositories]
        }

    def __repr__(self) -> str:
        return f"<RepositoryRegistry: {len(self.repositories)} repos>"
