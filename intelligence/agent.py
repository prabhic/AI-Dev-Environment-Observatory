"""
Intelligence Agent

LLM orchestration for generating insights.

Growth hooks:
- Today: Single Anthropic call
- Tomorrow: Multi-agent system with specialized agents
- Future: ML-based pattern recognition
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import anthropic
from rich.console import Console

from intelligence.models import (
    ArchitecturalInsight,
    CrossPatternInsight,
    LLMStrategy,
    Pattern,
    ComponentAnalysis
)

console = Console()


class IntelligenceAgent:
    """
    LLM-powered insight generation

    Growth-ready:
    - Today: Single LLM call for synthesis
    - Phase 2: Multi-agent system (architectural, pattern, evolution agents)
    - Phase 3: Fine-tuned models for pattern recognition
    """

    def __init__(self, config: Dict):
        self.config = config
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            console.print("[yellow]⚠[/yellow] ANTHROPIC_API_KEY not set. LLM synthesis will be skipped.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=api_key)

        self.model = config.get("llm_model", "claude-sonnet-4-20250514")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.3)

        # Load prompts
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates"""
        prompts_dir = Path("intelligence/prompts")
        prompts = {}

        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.txt"):
                prompt_name = prompt_file.stem
                with open(prompt_file, 'r') as f:
                    prompts[prompt_name] = f.read()

        return prompts

    def synthesize_insights(
        self,
        repo_data: Dict,
        analysis_results: Dict
    ) -> ArchitecturalInsight:
        """
        Synthesize raw analysis into architectural insights

        Args:
            repo_data: Repository metadata
            analysis_results: Raw analysis from all analyzers

        Returns:
            ArchitecturalInsight with LLM-generated insights
        """
        start_time = datetime.now()

        console.print(f"[cyan]🧠[/cyan] Synthesizing insights for {repo_data['name']}...")

        # If no LLM client, return basic insights
        if not self.client:
            return self._create_fallback_insights(repo_data, analysis_results)

        # Prepare prompt
        prompt = self._prepare_architectural_prompt(repo_data, analysis_results)

        try:
            # Call LLM
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse response
            response_text = response.content[0].text

            # Extract JSON from response
            llm_insights = self._extract_json(response_text)

            # Create insight object
            insight = self._build_insight(repo_data, analysis_results, llm_insights)

            # Update metadata
            duration = (datetime.now() - start_time).total_seconds()
            insight.analysis_metadata["analysis_duration_seconds"] = duration
            insight.analysis_metadata["llm_calls"] = 1

            console.print(f"[green]✓[/green] Insights generated for {repo_data['name']}")

            return insight

        except Exception as e:
            console.print(f"[red]✗[/red] Failed to generate insights: {e}")
            return self._create_fallback_insights(repo_data, analysis_results)

    def _prepare_architectural_prompt(self, repo_data: Dict, analysis: Dict) -> str:
        """Prepare prompt for architectural analysis"""
        template = self.prompts.get("v1_architectural", "")

        # Format analysis data
        analysis_summary = json.dumps({
            "components": analysis.get("components", {}).get("components", [])[:20],
            "patterns": analysis.get("patterns", {}).get("patterns", []),
            "llm_integration": analysis.get("llm_integration", {})
        }, indent=2)

        return template.format(
            repo_name=repo_data.get("name", ""),
            repo_type=repo_data.get("type", ""),
            primary_language=repo_data.get("language", ""),
            focus_areas=", ".join(repo_data.get("focus_areas", [])),
            analysis_data=analysis_summary
        )

    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from LLM response"""
        # Try to find JSON in response
        try:
            # Remove markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            return json.loads(text.strip())
        except:
            # Fallback: try to parse entire response
            try:
                return json.loads(text)
            except:
                return {}

    def _build_insight(
        self,
        repo_data: Dict,
        analysis: Dict,
        llm_insights: Dict
    ) -> ArchitecturalInsight:
        """Build ArchitecturalInsight from LLM response"""

        # Extract components from analysis
        components = []
        for comp_data in analysis.get("components", {}).get("components", [])[:30]:
            components.append(ComponentAnalysis(
                name=comp_data.get("name", ""),
                purpose=comp_data.get("type", ""),
                file_path=comp_data.get("file_path", ""),
                key_patterns=comp_data.get("patterns", []),
                complexity=comp_data.get("complexity", "medium"),
                reusability_score=5
            ))

        # Extract patterns
        patterns = []
        for pattern_data in analysis.get("patterns", {}).get("patterns", []):
            patterns.append(Pattern(
                name=pattern_data.get("name", ""),
                category=pattern_data.get("category", "other"),
                description=f"Found in {pattern_data.get('occurrences', 0)} locations",
                code_example=pattern_data.get("example", "")
            ))

        # Build LLM strategy
        llm_data = llm_insights.get("llm_strategy", {})
        llm_strategy = LLMStrategy(
            providers=llm_data.get("providers", []),
            streaming=llm_data.get("streaming", False),
            tool_calling=llm_data.get("tool_calling", False),
            context_optimization=llm_data.get("context_optimization", ""),
            prompt_engineering=llm_data.get("prompt_engineering")
        )

        return ArchitecturalInsight(
            repo_id=repo_data["id"],
            architecture_style=llm_insights.get("architecture_style", repo_data.get("type", "")),
            primary_language=repo_data.get("language", ""),
            key_dependencies=llm_insights.get("key_dependencies", []),
            description=llm_insights.get("description", ""),
            components=components,
            llm_strategy=llm_strategy,
            patterns=patterns,
            key_insights=llm_insights.get("key_insights", []),
            analysis_metadata={
                "files_analyzed": analysis.get("components", {}).get("total_files_analyzed", 0),
                "llm_calls": 0,  # Will be updated
                "confidence": 0.8
            }
        )

    def _create_fallback_insights(
        self,
        repo_data: Dict,
        analysis: Dict
    ) -> ArchitecturalInsight:
        """Create basic insights without LLM (fallback)"""

        # Basic component extraction
        components = []
        for comp_data in analysis.get("components", {}).get("components", [])[:30]:
            components.append(ComponentAnalysis(
                name=comp_data.get("name", ""),
                purpose=comp_data.get("type", ""),
                file_path=comp_data.get("file_path", ""),
                key_patterns=comp_data.get("patterns", []),
                complexity=comp_data.get("complexity", "medium")
            ))

        # Basic patterns
        patterns = []
        for pattern_data in analysis.get("patterns", {}).get("patterns", []):
            patterns.append(Pattern(
                name=pattern_data.get("name", ""),
                category=pattern_data.get("category", "other"),
                description=f"Detected {pattern_data.get('occurrences', 0)} times"
            ))

        # Basic LLM strategy from analysis
        llm_analysis = analysis.get("llm_integration", {})
        llm_strategy = LLMStrategy(
            providers=llm_analysis.get("providers", []),
            streaming=llm_analysis.get("streaming", False),
            tool_calling=llm_analysis.get("tool_calling", False),
            context_optimization=", ".join(llm_analysis.get("context_strategies", []))
        )

        return ArchitecturalInsight(
            repo_id=repo_data["id"],
            architecture_style=repo_data.get("type", ""),
            primary_language=repo_data.get("language", ""),
            description=f"AI-IDE project: {repo_data.get('name', '')}",
            components=components,
            llm_strategy=llm_strategy,
            patterns=patterns,
            key_insights=[
                "Analysis performed without LLM synthesis",
                f"Detected {len(patterns)} patterns",
                f"Analyzed {len(components)} components"
            ]
        )

    def extract_cross_patterns(self, all_insights: list) -> list:
        """
        [Future] Extract patterns across multiple repositories

        Growth hook: Multi-agent pattern analysis
        """
        console.print("[cyan]🔍[/cyan] Extracting cross-repository patterns...")

        # For MVP: Simple pattern aggregation
        # Future: LLM-powered cross-analysis

        pattern_map = {}

        for insight in all_insights:
            for pattern in insight.get("patterns", []):
                pattern_name = pattern.get("name", "")
                if pattern_name not in pattern_map:
                    pattern_map[pattern_name] = {
                        "repos": [],
                        "category": pattern.get("category", "other"),
                        "occurrences": 0
                    }

                pattern_map[pattern_name]["repos"].append(insight["repo_id"])
                pattern_map[pattern_name]["occurrences"] += pattern.get("prevalence", 1)

        # Build cross-patterns
        cross_patterns = []
        for pattern_name, data in pattern_map.items():
            if len(data["repos"]) >= 2:  # Only patterns in 2+ repos
                cross_patterns.append({
                    "pattern_id": pattern_name.replace(" ", "-").lower(),
                    "name": pattern_name,
                    "category": data["category"],
                    "description": f"Pattern found across {len(data['repos'])} repositories",
                    "implementations": [
                        {"repo_id": repo_id, "approach": "Detected in code analysis"}
                        for repo_id in data["repos"]
                    ],
                    "metadata": {
                        "prevalence": len(data["repos"]),
                        "maturity": "established" if len(data["repos"]) >= 3 else "emerging"
                    }
                })

        console.print(f"[green]✓[/green] Found {len(cross_patterns)} cross-repository patterns")

        return cross_patterns
