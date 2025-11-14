"""
Repository Registry Models

Pydantic models for type-safe repository metadata.
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Literal
from datetime import datetime


class Repository(BaseModel):
    """Repository metadata model"""

    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Human-readable name")
    url: str = Field(..., description="Git clone URL")
    type: Literal[
        "vscode-extension",
        "multi-ide-extension",
        "cli-agent",
        "web-ide",
        "framework"
    ]
    language: str = Field(..., description="Primary programming language")
    focus_areas: List[str] = Field(default_factory=list)
    analysis_priority: Literal["low", "medium", "high", "critical"] = "medium"
    tags: List[str] = Field(default_factory=list)

    # [Future] Fields - will be populated by monitoring system
    last_analyzed: Optional[datetime] = None
    health_status: Optional[Literal["active", "stale", "archived"]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cline",
                "name": "Cline (formerly Claude Dev)",
                "url": "https://github.com/cline/cline",
                "type": "vscode-extension",
                "language": "typescript",
                "focus_areas": ["llm_integration", "diff_application"],
                "analysis_priority": "high",
                "tags": ["agentic", "vscode", "anthropic"]
            }
        }


class RegistryMetadata(BaseModel):
    """Registry-level metadata"""

    auto_discovery: bool = False
    monitoring_enabled: bool = False


class DiscoveryConfig(BaseModel):
    """
    [Future] Auto-discovery configuration

    When enabled, will scan GitHub for new AI-IDE repos.
    """

    enabled: bool = False
    sources: Optional[List[dict]] = None
    filters: Optional[dict] = None


class RegistrySchema(BaseModel):
    """Complete registry schema"""

    version: str
    last_updated: str
    registry: RegistryMetadata
    repositories: List[Repository]
    discovery: Optional[DiscoveryConfig] = None
