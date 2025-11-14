"""
Component Analyzer

Extracts architectural components from repository.

Growth hooks:
- Can use AST parsing for more accurate analysis
- Can detect component relationships
- Can score component importance
"""

from pathlib import Path
from typing import Dict, List
from analyzers.core.base_analyzer import BaseAnalyzer
from analyzers.core.file_scanner import FileScanner


class ComponentAnalyzer(BaseAnalyzer):
    """
    Analyze repository structure and identify key components

    Today: File-based heuristics
    Tomorrow: AST parsing, dependency graph analysis
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.scanner = FileScanner(
            max_file_size_kb=config.get("file_size_limit_kb", 500)
        )

    def get_name(self) -> str:
        return "ComponentAnalyzer"

    def analyze(self, repo_path: Path, file_data: Dict) -> Dict:
        """Extract architectural components"""
        components = []

        # Analyze priority files first (most important)
        for file_path in file_data["priority_files"][:30]:  # Limit for performance
            component = self._analyze_file(file_path, repo_path)
            if component:
                components.append(component)

        # Analyze some regular files for completeness
        for file_path in file_data["regular_files"][:20]:
            component = self._analyze_file(file_path, repo_path)
            if component:
                components.append(component)

        return {
            "components": components,
            "total_files_analyzed": len(components),
            "component_types": self._categorize_components(components)
        }

    def _analyze_file(self, file_path: Path, repo_path: Path) -> Dict:
        """Analyze a single file and extract component info"""
        rel_path = file_path.relative_to(repo_path)
        content = self.scanner.get_file_content(file_path)

        if not content:
            return None

        # Extract basic metadata
        component = {
            "name": file_path.stem,
            "file_path": str(rel_path),
            "extension": file_path.suffix,
            "size_bytes": len(content),
            "lines": len(content.split("\n"))
        }

        # Detect component type based on patterns
        component["type"] = self._detect_component_type(file_path, content)

        # Extract key patterns
        component["patterns"] = self._extract_patterns(content, file_path.suffix)

        # Simple complexity estimate
        component["complexity"] = self._estimate_complexity(content)

        return component

    def _detect_component_type(self, file_path: Path, content: str) -> str:
        """Detect what kind of component this is"""
        name_lower = file_path.name.lower()
        content_lower = content.lower()

        # Entry point
        if "main" in name_lower or "index" in name_lower:
            return "entry_point"

        # Extension-specific
        if "extension" in name_lower or "activate" in content_lower:
            return "extension_core"

        # LLM/AI related
        if any(kw in name_lower for kw in ["llm", "ai", "agent", "chat", "completion"]):
            return "llm_integration"

        # API/Service
        if any(kw in name_lower for kw in ["api", "service", "client"]):
            return "api_service"

        # UI/View
        if any(kw in name_lower for kw in ["view", "component", "ui"]):
            return "ui_component"

        # Utility
        if any(kw in name_lower for kw in ["util", "helper", "tool"]):
            return "utility"

        # Configuration
        if file_path.suffix in [".json", ".yaml", ".yml", ".toml"]:
            return "configuration"

        return "other"

    def _extract_patterns(self, content: str, extension: str) -> List[str]:
        """Extract coding patterns from content"""
        patterns = []

        # Detect async patterns
        if "async " in content or "await " in content:
            patterns.append("async_programming")

        # Detect streaming
        if "stream" in content.lower():
            patterns.append("streaming")

        # Detect event handling
        if "event" in content.lower() or "listener" in content.lower():
            patterns.append("event_driven")

        # Detect class-based
        if "class " in content:
            patterns.append("object_oriented")

        # Detect functional
        if extension in [".ts", ".js"] and "=>" in content:
            patterns.append("functional_programming")

        return patterns

    def _estimate_complexity(self, content: str) -> str:
        """Simple complexity estimation"""
        lines = len(content.split("\n"))

        if lines < 50:
            return "low"
        elif lines < 200:
            return "medium"
        else:
            return "high"

    def _categorize_components(self, components: List[Dict]) -> Dict:
        """Categorize components by type"""
        categories = {}
        for comp in components:
            comp_type = comp.get("type", "other")
            categories[comp_type] = categories.get(comp_type, 0) + 1
        return categories
