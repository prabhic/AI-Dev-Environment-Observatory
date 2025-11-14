"""
Base Analyzer Interface

Abstract base for all analyzers.

Growth pattern: New analyzers can be added by extending this base.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseAnalyzer(ABC):
    """
    Abstract base for all analyzers

    Growth pattern:
    - Each analyzer implements this interface
    - Orchestrator can run all analyzers uniformly
    - New analyzers can be added without changing orchestrator
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def analyze(self, repo_path: Path, file_data: Dict) -> Dict:
        """
        Analyze repository and return insights

        Args:
            repo_path: Path to local repository
            file_data: Dictionary from FileScanner with priority/regular files

        Returns:
            Dictionary of analysis results
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return analyzer name for logging"""
        pass

    def should_run(self, repo: Any) -> bool:
        """
        Determine if this analyzer should run for a given repository

        Growth hook: Can add conditional execution based on:
        - Repository type
        - Language
        - Previous analysis results
        - Resource availability
        """
        return True

    def merge_results(self, existing: Dict, new: Dict) -> Dict:
        """
        [Future] Merge incremental analysis results

        Growth hook: For incremental analysis mode
        """
        return {**existing, **new}
