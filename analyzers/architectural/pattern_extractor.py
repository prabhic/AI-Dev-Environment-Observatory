"""
Pattern Extractor

Extracts code patterns and architectural patterns from repositories.

Growth hooks:
- Today: Heuristic-based pattern detection
- Tomorrow: ML-based pattern recognition
- Future: Pattern evolution tracking
"""

from pathlib import Path
from typing import Dict, List
from analyzers.core.base_analyzer import BaseAnalyzer
from analyzers.core.file_scanner import FileScanner


class PatternExtractor(BaseAnalyzer):
    """
    Extract architectural and code patterns

    Identifies:
    - LLM integration patterns
    - State management patterns
    - Streaming patterns
    - Tool calling patterns
    - Context management patterns
    """

    # Pattern signatures to look for
    PATTERN_SIGNATURES = {
        "streaming_responses": [
            "stream",
            "chunk",
            "sse",
            "eventstream"
        ],
        "tool_calling": [
            "tool",
            "function_call",
            "execute_tool",
            "tool_use"
        ],
        "context_management": [
            "context",
            "history",
            "conversation",
            "memory"
        ],
        "diff_application": [
            "diff",
            "patch",
            "apply",
            "merge"
        ],
        "file_operations": [
            "writeFile",
            "readFile",
            "fs.",
            "filesystem"
        ],
        "async_execution": [
            "async",
            "await",
            "promise",
            "asyncio"
        ],
        "event_driven": [
            "event",
            "listener",
            "emit",
            "dispatch"
        ],
        "state_management": [
            "state",
            "store",
            "reducer",
            "context"
        ]
    }

    def __init__(self, config: Dict):
        super().__init__(config)
        self.scanner = FileScanner()

    def get_name(self) -> str:
        return "PatternExtractor"

    def analyze(self, repo_path: Path, file_data: Dict) -> Dict:
        """Extract patterns from repository"""
        pattern_occurrences = {}
        code_examples = {}

        # Analyze priority files for patterns
        all_files = file_data["priority_files"] + file_data["regular_files"]

        for file_path in all_files[:50]:  # Limit for performance
            content = self.scanner.get_file_content(file_path)
            if not content:
                continue

            # Check for each pattern signature
            for pattern_name, keywords in self.PATTERN_SIGNATURES.items():
                if self._detect_pattern(content, keywords):
                    if pattern_name not in pattern_occurrences:
                        pattern_occurrences[pattern_name] = {
                            "count": 0,
                            "files": []
                        }

                    pattern_occurrences[pattern_name]["count"] += 1
                    pattern_occurrences[pattern_name]["files"].append(
                        str(file_path.relative_to(repo_path))
                    )

                    # Extract code example (first occurrence)
                    if pattern_name not in code_examples:
                        example = self._extract_code_example(content, keywords)
                        if example:
                            code_examples[pattern_name] = example

        # Build pattern summary
        patterns = []
        for pattern_name, data in pattern_occurrences.items():
            patterns.append({
                "name": pattern_name,
                "category": self._categorize_pattern(pattern_name),
                "occurrences": data["count"],
                "files": data["files"][:5],  # Limit file list
                "example": code_examples.get(pattern_name, "")
            })

        return {
            "patterns": patterns,
            "pattern_count": len(patterns),
            "total_occurrences": sum(p["occurrences"] for p in patterns)
        }

    def _detect_pattern(self, content: str, keywords: List[str]) -> bool:
        """Check if any keyword appears in content"""
        content_lower = content.lower()
        return any(keyword.lower() in content_lower for keyword in keywords)

    def _extract_code_example(self, content: str, keywords: List[str]) -> str:
        """Extract a small code snippet showing the pattern"""
        lines = content.split("\n")

        for i, line in enumerate(lines):
            # Find line with keyword
            if any(kw.lower() in line.lower() for kw in keywords):
                # Extract 5 lines of context
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                example = "\n".join(lines[start:end])

                # Truncate if too long
                if len(example) > 500:
                    example = example[:500] + "..."

                return example

        return ""

    def _categorize_pattern(self, pattern_name: str) -> str:
        """Categorize pattern into broader category"""
        if "llm" in pattern_name or "stream" in pattern_name or "tool" in pattern_name:
            return "llm_integration"
        elif "context" in pattern_name or "history" in pattern_name:
            return "context_management"
        elif "state" in pattern_name or "store" in pattern_name:
            return "state_management"
        elif "file" in pattern_name or "diff" in pattern_name:
            return "file_operations"
        elif "async" in pattern_name or "event" in pattern_name:
            return "concurrency"
        else:
            return "other"
