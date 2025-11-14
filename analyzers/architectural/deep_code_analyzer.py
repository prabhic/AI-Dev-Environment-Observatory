"""
Deep Code Analyzer

Extracts actual code examples and architectural patterns.

This analyzer goes deeper than keyword matching - it finds the actual
implementation of key patterns.
"""

from pathlib import Path
from typing import Dict, List, Optional
from analyzers.core.base_analyzer import BaseAnalyzer
from analyzers.core.file_scanner import FileScanner


class DeepCodeAnalyzer(BaseAnalyzer):
    """
    Extract code examples of key architectural patterns

    Focus areas:
    - LLM integration code
    - Context management logic
    - Edit application mechanisms
    - Tool calling implementation
    """

    # Patterns to extract with context
    KEY_PATTERNS = {
        "llm_call": {
            "keywords": ["createMessage", "chat.completions", "messages.create", "complete"],
            "context_lines": 20
        },
        "streaming": {
            "keywords": ["stream", "onChunk", "SSE", "EventSource"],
            "context_lines": 15
        },
        "context_management": {
            "keywords": ["truncate", "summarize", "context_window", "trim_messages"],
            "context_lines": 20
        },
        "tool_calling": {
            "keywords": ["tool_use", "function_call", "execute_tool", "tools:"],
            "context_lines": 25
        },
        "edit_application": {
            "keywords": ["applyDiff", "applyEdit", "search_replace", "patch"],
            "context_lines": 30
        }
    }

    def __init__(self, config: Dict):
        super().__init__(config)
        self.scanner = FileScanner()

    def get_name(self) -> str:
        return "DeepCodeAnalyzer"

    def analyze(self, repo_path: Path, file_data: Dict) -> Dict:
        """Extract code examples of key patterns"""
        code_examples = {}

        # Prioritize likely files
        priority_files = self._get_priority_files(file_data, repo_path)

        for pattern_name, pattern_config in self.KEY_PATTERNS.items():
            examples = self._find_pattern_examples(
                priority_files,
                pattern_config["keywords"],
                pattern_config["context_lines"],
                repo_path
            )

            if examples:
                code_examples[pattern_name] = {
                    "found": True,
                    "examples": examples[:3],  # Top 3 examples
                    "total_occurrences": len(examples)
                }
            else:
                code_examples[pattern_name] = {
                    "found": False,
                    "examples": [],
                    "total_occurrences": 0
                }

        return {
            "code_examples": code_examples,
            "files_scanned": len(priority_files)
        }

    def _get_priority_files(self, file_data: Dict, repo_path: Path) -> List[Path]:
        """Get files most likely to contain key patterns"""
        priority = []

        # Files with LLM/AI keywords in name
        for file in file_data["priority_files"] + file_data["regular_files"]:
            name_lower = file.name.lower()
            if any(kw in name_lower for kw in [
                "llm", "ai", "agent", "chat", "api", "client",
                "completion", "message", "stream", "tool", "edit", "diff"
            ]):
                priority.append(file)

        # Add some priority files
        for file in file_data["priority_files"]:
            if file not in priority:
                priority.append(file)

        return priority[:50]  # Limit for performance

    def _find_pattern_examples(
        self,
        files: List[Path],
        keywords: List[str],
        context_lines: int,
        repo_path: Path
    ) -> List[Dict]:
        """Find code examples matching pattern"""
        examples = []

        for file_path in files:
            content = self.scanner.get_file_content(file_path)
            if not content:
                continue

            lines = content.split("\n")

            for i, line in enumerate(lines):
                # Check if any keyword matches
                if any(kw.lower() in line.lower() for kw in keywords):
                    # Extract with context
                    start = max(0, i - context_lines // 2)
                    end = min(len(lines), i + context_lines // 2)

                    snippet = "\n".join(lines[start:end])

                    # Calculate relevance score
                    score = self._score_snippet(snippet, keywords)

                    examples.append({
                        "file": str(file_path.relative_to(repo_path)),
                        "line_start": start + 1,
                        "line_end": end + 1,
                        "matched_line": i + 1,
                        "snippet": snippet,
                        "score": score
                    })

        # Sort by score and return top examples
        examples.sort(key=lambda x: x["score"], reverse=True)
        return examples

    def _score_snippet(self, snippet: str, keywords: List[str]) -> float:
        """Score snippet by relevance"""
        score = 0.0

        # More keywords = higher score
        for keyword in keywords:
            count = snippet.lower().count(keyword.lower())
            score += count * 2

        # Longer snippets with actual code = higher score
        if "{" in snippet or "(" in snippet:
            score += 5

        # Has function definition = higher score
        if "function" in snippet or "def " in snippet or "const " in snippet:
            score += 10

        # Has async = higher score for LLM patterns
        if "async" in snippet or "await" in snippet:
            score += 3

        # Has error handling = more complete example
        if "try" in snippet or "catch" in snippet or "except" in snippet:
            score += 5

        return score
