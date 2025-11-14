"""
Smart File Scanner

Intelligently identifies important files for analysis.

Growth hooks:
- Smart filtering based on file patterns
- Configurable file size limits
- Priority scoring for files
"""

from pathlib import Path
from typing import List, Dict, Set
import pathspec
from rich.console import Console

console = Console()


class FileScanner:
    """
    Intelligently scan repositories for analysis-worthy files

    Growth-ready:
    - Today: Pattern-based filtering, size limits
    - Phase 2: ML-based importance scoring
    - Phase 3: Incremental scanning (only changed files)
    """

    # File patterns to always include (high-value files)
    PRIORITY_PATTERNS = [
        # Core architecture
        "**/package.json",
        "**/tsconfig.json",
        "**/pyproject.toml",
        "**/setup.py",
        "**/Cargo.toml",

        # Entry points
        "**/main.ts",
        "**/main.js",
        "**/index.ts",
        "**/index.js",
        "**/__init__.py",
        "**/main.py",

        # Extension manifests
        "**/extension.ts",
        "**/extension.js",
        "**/manifest.json",
        "**/package.json",

        # LLM integration (likely locations)
        "**/llm*.ts",
        "**/llm*.py",
        "**/ai*.ts",
        "**/ai*.py",
        "**/agent*.ts",
        "**/agent*.py",
        "**/chat*.ts",
        "**/chat*.py",
        "**/api*.ts",
        "**/api*.py",
    ]

    # Directories to skip
    SKIP_DIRS = {
        "node_modules",
        ".git",
        "dist",
        "build",
        "out",
        "__pycache__",
        ".venv",
        "venv",
        "target",
        ".next",
        "coverage",
        ".pytest_cache",
    }

    # File extensions to include
    INCLUDE_EXTENSIONS = {
        ".ts", ".tsx", ".js", ".jsx",
        ".py",
        ".rs",
        ".go",
        ".java",
        ".json", ".yaml", ".yml", ".toml",
    }

    def __init__(self, max_file_size_kb: int = 500):
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.priority_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            self.PRIORITY_PATTERNS
        )

    def scan_repository(self, repo_path: Path, max_files: int = 100) -> Dict:
        """
        Scan repository and return important files

        Args:
            repo_path: Path to repository
            max_files: Maximum number of files to return

        Returns:
            Dictionary with priority and regular files
        """
        priority_files = []
        regular_files = []

        # Load .gitignore if present
        gitignore_spec = self._load_gitignore(repo_path)

        for file_path in repo_path.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip if in excluded directory
            if any(skip_dir in file_path.parts for skip_dir in self.SKIP_DIRS):
                continue

            # Skip if in .gitignore
            rel_path = file_path.relative_to(repo_path)
            if gitignore_spec and gitignore_spec.match_file(str(rel_path)):
                continue

            # Skip if wrong extension
            if file_path.suffix not in self.INCLUDE_EXTENSIONS:
                continue

            # Skip if too large
            if file_path.stat().st_size > self.max_file_size_bytes:
                continue

            # Categorize
            if self.priority_spec.match_file(str(rel_path)):
                priority_files.append(file_path)
            else:
                regular_files.append(file_path)

        # Sort by likely importance
        priority_files = sorted(priority_files, key=lambda p: len(p.parts))
        regular_files = sorted(regular_files, key=lambda p: len(p.parts))

        # Limit total files
        total_priority = len(priority_files)
        remaining = max_files - total_priority
        regular_files = regular_files[:remaining]

        console.print(
            f"[cyan]📁[/cyan] Scanned {repo_path.name}: "
            f"{total_priority} priority, {len(regular_files)} regular files"
        )

        return {
            "priority_files": priority_files,
            "regular_files": regular_files,
            "total_files": total_priority + len(regular_files),
            "skipped_large_files": self._count_large_files(repo_path)
        }

    def _load_gitignore(self, repo_path: Path) -> pathspec.PathSpec:
        """Load .gitignore patterns"""
        gitignore_path = repo_path / ".gitignore"
        if not gitignore_path.exists():
            return None

        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()

        return pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern,
            patterns
        )

    def _count_large_files(self, repo_path: Path) -> int:
        """Count files that were skipped due to size"""
        # Simplified - could be more accurate
        return 0

    def get_file_content(self, file_path: Path) -> str:
        """
        Read file content safely

        Growth hook: Can add encoding detection, binary file handling
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return ""
        except:
            return ""

    def extract_imports(self, file_path: Path, language: str) -> List[str]:
        """
        Extract import statements to understand dependencies

        Growth hook: Can use AST parsing for more accurate extraction
        """
        content = self.get_file_content(file_path)
        imports = []

        if language == "typescript" or language == "javascript":
            # Simple regex-based extraction
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    imports.append(line)

        elif language == "python":
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    imports.append(line)

        return imports[:50]  # Limit for performance
