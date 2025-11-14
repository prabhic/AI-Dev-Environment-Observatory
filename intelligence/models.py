"""
Intelligence Layer Data Models

Pydantic models for type-safe LLM responses and insights.

Growth-ready: All models support optional fields for future features.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime


class ComponentAnalysis(BaseModel):
    """Analysis of a single architectural component"""

    name: str = Field(..., description="Component name")
    purpose: str = Field(..., description="What this component does")
    file_path: str = Field(..., description="Relative file path")
    key_patterns: List[str] = Field(
        default_factory=list,
        description="Key patterns used in this component"
    )
    complexity: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Complexity assessment"
    )
    reusability_score: int = Field(
        ge=0, le=10,
        default=5,
        description="How reusable is this component (0-10)"
    )
    llm_integration: Optional[Dict] = Field(
        default=None,
        description="LLM integration details if applicable"
    )


class LLMStrategy(BaseModel):
    """How the repository integrates with LLMs"""

    providers: List[str] = Field(
        default_factory=list,
        description="LLM providers used (anthropic, openai, etc.)"
    )
    streaming: bool = Field(
        default=False,
        description="Whether streaming responses is supported"
    )
    tool_calling: bool = Field(
        default=False,
        description="Whether tool/function calling is used"
    )
    context_optimization: str = Field(
        default="",
        description="Strategy for managing context/conversation"
    )
    prompt_engineering: Optional[str] = Field(
        default=None,
        description="Notable prompt engineering techniques"
    )


class Pattern(BaseModel):
    """A code or architectural pattern"""

    name: str
    category: str
    description: str
    code_example: Optional[str] = None
    prevalence: Optional[int] = Field(
        default=1,
        description="How many times this pattern appears"
    )


class ArchitecturalInsight(BaseModel):
    """Complete analysis of a repository"""

    repo_id: str
    analyzed_at: datetime = Field(default_factory=datetime.now)
    version: str = "1.0"

    # Core architecture
    architecture_style: str = Field(
        ...,
        description="Overall architecture (extension, cli-agent, web-ide, etc.)"
    )
    primary_language: str
    key_dependencies: List[str] = Field(default_factory=list)
    description: Optional[str] = Field(
        default=None,
        description="High-level description of the project"
    )

    # Components
    components: List[ComponentAnalysis] = Field(default_factory=list)

    # LLM Strategy
    llm_strategy: LLMStrategy = Field(default_factory=LLMStrategy)

    # Patterns
    patterns: List[Pattern] = Field(default_factory=list)

    # Key insights
    key_insights: List[str] = Field(
        default_factory=list,
        description="Notable insights about the architecture"
    )

    # Metadata
    analysis_metadata: Dict = Field(
        default_factory=lambda: {
            "files_analyzed": 0,
            "llm_calls": 0,
            "confidence": 0.0,
            "analysis_duration_seconds": 0
        }
    )

    # [Future] Evolution data
    evolution_data: Optional[Dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CrossPatternInsight(BaseModel):
    """Pattern observed across multiple repositories"""

    pattern_id: str
    name: str
    category: Literal[
        "llm_integration",
        "context_management",
        "streaming",
        "tool_calling",
        "diff_application",
        "file_operations",
        "state_management",
        "extension_architecture",
        "agent_architecture",
        "error_handling"
    ]
    description: str

    # Implementations across repos
    implementations: List[Dict] = Field(
        default_factory=list,
        description="How each repo implements this pattern"
    )

    # Evolution tracking [Future]
    evolution: Optional[List[Dict]] = None

    # Metadata
    metadata: Dict = Field(
        default_factory=lambda: {
            "first_seen": "",
            "prevalence": 0,
            "maturity": "emerging"
        }
    )


class EvolutionSnapshot(BaseModel):
    """
    [Future] Snapshot of a repository at a point in time

    For tracking how repositories evolve over time.
    """

    repo_id: str
    snapshot_date: datetime
    git_commit: str
    insights: ArchitecturalInsight
    changes_since_last: Optional[Dict] = None


class AnalysisRun(BaseModel):
    """Metadata about an analysis run"""

    run_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    repos_analyzed: List[str] = Field(default_factory=list)
    total_repos: int = 0
    successful: int = 0
    failed: int = 0
    errors: List[str] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
