"""
Storage Layer

Manages persisting and loading analysis data.

Growth hooks:
- Today: JSON files with versioning
- Tomorrow: PostgreSQL/TimescaleDB
- Future: Time-series data for evolution tracking

Easy to swap: Just implement StorageBackend interface
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod
from rich.console import Console

from intelligence.models import ArchitecturalInsight, AnalysisRun

console = Console()


class StorageBackend(ABC):
    """
    Abstract storage backend

    Growth pattern: Different storage implementations (JSON, SQL, etc.)
    share this interface for easy swapping
    """

    @abstractmethod
    def save_insight(self, repo_id: str, insight: ArchitecturalInsight) -> None:
        pass

    @abstractmethod
    def load_insight(self, repo_id: str) -> Optional[ArchitecturalInsight]:
        pass

    @abstractmethod
    def save_patterns(self, patterns: List[Dict]) -> None:
        pass

    @abstractmethod
    def load_patterns(self) -> List[Dict]:
        pass

    @abstractmethod
    def save_metadata(self, metadata: Dict) -> None:
        pass

    @abstractmethod
    def load_metadata(self) -> Optional[Dict]:
        pass


class JSONStorage(StorageBackend):
    """
    JSON file storage implementation

    Today: Simple JSON files
    Tomorrow: Easily swap for database storage
    """

    def __init__(self, base_path: str = "storage", version: str = "v1"):
        self.base_path = Path(base_path)
        self.version = version
        self.insights_path = self.base_path / "insights" / version
        self.patterns_path = self.base_path / "patterns"

        # Ensure directories exist
        self.insights_path.mkdir(parents=True, exist_ok=True)
        self.patterns_path.mkdir(parents=True, exist_ok=True)

    def save_insight(self, repo_id: str, insight: ArchitecturalInsight) -> None:
        """Save repository insights to JSON"""
        repo_dir = self.insights_path / repo_id
        repo_dir.mkdir(exist_ok=True)

        insight_path = repo_dir / "insights.json"

        # Convert to dict and save
        insight_data = insight.model_dump()

        with open(insight_path, 'w') as f:
            json.dump(insight_data, f, indent=2, default=str)

        console.print(f"[green]✓[/green] Saved insights for {repo_id}")

    def load_insight(self, repo_id: str) -> Optional[ArchitecturalInsight]:
        """Load repository insights from JSON"""
        insight_path = self.insights_path / repo_id / "insights.json"

        if not insight_path.exists():
            return None

        with open(insight_path, 'r') as f:
            data = json.load(f)

        return ArchitecturalInsight(**data)

    def load_all_insights(self) -> List[Dict]:
        """Load all repository insights"""
        insights = []

        for repo_dir in self.insights_path.iterdir():
            if repo_dir.is_dir():
                insight_file = repo_dir / "insights.json"
                if insight_file.exists():
                    with open(insight_file, 'r') as f:
                        insights.append(json.load(f))

        return insights

    def save_patterns(self, patterns: List[Dict]) -> None:
        """Save cross-repository patterns"""
        patterns_file = self.patterns_path / f"{self.version}_patterns.json"

        with open(patterns_file, 'w') as f:
            json.dump({
                "version": self.version,
                "generated_at": datetime.now().isoformat(),
                "patterns": patterns
            }, f, indent=2)

        console.print(f"[green]✓[/green] Saved {len(patterns)} cross-patterns")

    def load_patterns(self) -> List[Dict]:
        """Load cross-repository patterns"""
        patterns_file = self.patterns_path / f"{self.version}_patterns.json"

        if not patterns_file.exists():
            return []

        with open(patterns_file, 'r') as f:
            data = json.load(f)
            return data.get("patterns", [])

    def save_metadata(self, metadata: Dict) -> None:
        """Save analysis run metadata"""
        metadata_file = self.insights_path / "metadata.json"

        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)

    def load_metadata(self) -> Optional[Dict]:
        """Load analysis run metadata"""
        metadata_file = self.insights_path / "metadata.json"

        if not metadata_file.exists():
            return None

        with open(metadata_file, 'r') as f:
            return json.load(f)

    def export_for_web(self, output_path: Path) -> None:
        """
        Export data in format optimized for web UI

        Creates a single JSON file with all data for static site generation
        """
        insights = self.load_all_insights()
        patterns = self.load_patterns()
        metadata = self.load_metadata()

        web_data = {
            "meta": {
                "version": self.version,
                "last_updated": datetime.now().isoformat(),
                "total_repos": len(insights)
            },
            "insights": insights,
            "patterns": patterns,
            "metadata": metadata
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(web_data, f, indent=2)

        console.print(f"[green]✓[/green] Exported data for web UI: {output_path}")


class PostgresStorage(StorageBackend):
    """
    [Future] PostgreSQL storage implementation

    Growth trigger: When time-series tracking is needed
    Effort: ~12 hours

    Benefits:
    - Queryable insights
    - Time-series evolution tracking
    - Better performance at scale
    """

    def __init__(self, connection_string: str):
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def save_insight(self, repo_id: str, insight: ArchitecturalInsight) -> None:
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def load_insight(self, repo_id: str) -> Optional[ArchitecturalInsight]:
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def save_patterns(self, patterns: List[Dict]) -> None:
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def load_patterns(self) -> List[Dict]:
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def save_metadata(self, metadata: Dict) -> None:
        raise NotImplementedError("PostgreSQL storage not yet enabled")

    def load_metadata(self) -> Optional[Dict]:
        raise NotImplementedError("PostgreSQL storage not yet enabled")


class StorageLayer:
    """
    Unified storage interface

    Growth-ready: Automatically uses configured backend
    """

    def __init__(self, config: Dict):
        storage_format = config.get("format", "json")
        version = "v1"

        if storage_format == "json":
            self.backend = JSONStorage(
                base_path=config.get("base_path", "storage"),
                version=version
            )
        elif storage_format == "postgres":
            # [Future] When enabled in config
            connection_string = config.get("postgres_connection", "")
            self.backend = PostgresStorage(connection_string)
        else:
            raise ValueError(f"Unknown storage format: {storage_format}")

    def save_insights(self, repo_id: str, insights: ArchitecturalInsight) -> None:
        """Save repository insights"""
        self.backend.save_insight(repo_id, insights)

    def load_insights(self, repo_id: str) -> Optional[ArchitecturalInsight]:
        """Load repository insights"""
        return self.backend.load_insight(repo_id)

    def get_all_insights(self) -> List[Dict]:
        """Load all insights"""
        if isinstance(self.backend, JSONStorage):
            return self.backend.load_all_insights()
        else:
            raise NotImplementedError("Not yet implemented for this backend")

    def save_patterns(self, patterns: List[Dict]) -> None:
        """Save cross-repository patterns"""
        self.backend.save_patterns(patterns)

    def load_patterns(self) -> List[Dict]:
        """Load cross-repository patterns"""
        return self.backend.load_patterns()

    def save_run_metadata(self, run: AnalysisRun) -> None:
        """Save analysis run metadata"""
        self.backend.save_metadata(run.model_dump())

    def export_for_web(self, output_path: str = "web/public/data/observatory.json") -> None:
        """Export data for web UI"""
        if isinstance(self.backend, JSONStorage):
            self.backend.export_for_web(Path(output_path))
        else:
            raise NotImplementedError("Web export not yet implemented for this backend")
