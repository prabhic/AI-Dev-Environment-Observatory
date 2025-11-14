"""
LLM Integration Analyzer

Specialized analyzer for understanding how repositories integrate with LLMs.

Growth hooks:
- Can detect specific LLM providers (Anthropic, OpenAI, etc.)
- Can analyze prompting strategies
- Can detect tool use patterns
"""

from pathlib import Path
from typing import Dict, List
from analyzers.core.base_analyzer import BaseAnalyzer
from analyzers.core.file_scanner import FileScanner


class LLMIntegrationAnalyzer(BaseAnalyzer):
    """
    Analyze LLM integration patterns

    Detects:
    - Which LLM providers are used
    - Streaming vs non-streaming
    - Tool calling support
    - Prompt engineering patterns
    - Context optimization strategies
    """

    # Provider detection patterns
    PROVIDERS = {
        "anthropic": ["anthropic", "claude", "messages.create"],
        "openai": ["openai", "gpt-", "chat.completions"],
        "google": ["gemini", "google.generativeai"],
        "cohere": ["cohere"],
        "local": ["ollama", "llama.cpp", "localai"]
    }

    def __init__(self, config: Dict):
        super().__init__(config)
        self.scanner = FileScanner()

    def get_name(self) -> str:
        return "LLMIntegrationAnalyzer"

    def analyze(self, repo_path: Path, file_data: Dict) -> Dict:
        """Analyze LLM integration strategy"""
        providers_found = set()
        streaming_detected = False
        tool_calling_detected = False
        context_strategies = []

        # Search through all files
        all_files = file_data["priority_files"] + file_data["regular_files"]

        for file_path in all_files[:60]:
            content = self.scanner.get_file_content(file_path)
            if not content:
                continue

            content_lower = content.lower()

            # Detect providers
            for provider, keywords in self.PROVIDERS.items():
                if any(kw in content_lower for kw in keywords):
                    providers_found.add(provider)

            # Detect streaming
            if any(kw in content_lower for kw in ["stream", "sse", "eventstream"]):
                streaming_detected = True

            # Detect tool calling
            if any(kw in content_lower for kw in ["tool", "function_call", "tool_use"]):
                tool_calling_detected = True

            # Detect context strategies
            if "context" in content_lower:
                if "window" in content_lower:
                    context_strategies.append("context_window_management")
                if "compress" in content_lower or "summarize" in content_lower:
                    context_strategies.append("context_compression")
                if "memory" in content_lower:
                    context_strategies.append("conversation_memory")

        return {
            "providers": list(providers_found),
            "multi_provider": len(providers_found) > 1,
            "streaming": streaming_detected,
            "tool_calling": tool_calling_detected,
            "context_strategies": list(set(context_strategies)),
            "llm_files": self._find_llm_files(all_files, repo_path)
        }

    def _find_llm_files(self, files: List[Path], repo_path: Path) -> List[str]:
        """Find files that likely contain LLM integration code"""
        llm_files = []

        for file_path in files:
            name_lower = file_path.name.lower()
            if any(kw in name_lower for kw in ["llm", "ai", "agent", "chat", "completion"]):
                llm_files.append(str(file_path.relative_to(repo_path)))

        return llm_files[:10]  # Limit
