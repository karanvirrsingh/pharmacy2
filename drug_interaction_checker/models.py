"""Data models for the Drug Interaction Checker."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):
    """Severity levels for drug interactions."""

    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    CONTRAINDICATED = "Contraindicated"

    def color(self) -> str:
        """Return a Rich-compatible color string for the severity level."""
        return {
            Severity.MINOR: "green",
            Severity.MODERATE: "yellow",
            Severity.MAJOR: "red",
            Severity.CONTRAINDICATED: "bold red",
        }[self]

    def emoji(self) -> str:
        """Return an emoji indicator for the severity level."""
        return {
            Severity.MINOR: "🟢",
            Severity.MODERATE: "🟡",
            Severity.MAJOR: "🔴",
            Severity.CONTRAINDICATED: "⛔",
        }[self]


@dataclass
class Drug:
    """Represents a drug with its primary name and known aliases."""

    name: str
    aliases: List[str] = field(default_factory=list)

    def all_names(self) -> List[str]:
        """Return a list of all known names (primary + aliases), lowercased."""
        return [n.lower() for n in [self.name] + self.aliases]


@dataclass
class Interaction:
    """Represents a drug–drug interaction entry."""

    drug1: str
    drug2: str
    description: str
    mechanism: str
    severity: Severity
    recommendation: str
    confidence: float = 1.0  # 0.0–1.0; 1.0 = confirmed database entry

    def drug_pair(self) -> tuple:
        """Return a canonical (sorted) pair of lowercase drug names."""
        return tuple(sorted([self.drug1.lower(), self.drug2.lower()]))


@dataclass
class InteractionResult:
    """The result returned to callers after an interaction lookup."""

    drug1_query: str
    drug2_query: str
    drug1_matched: Optional[str]
    drug2_matched: Optional[str]
    interaction: Optional[Interaction] = None
    confidence: float = 0.0
    message: str = ""

    @property
    def found(self) -> bool:
        """True when an interaction record was found."""
        return self.interaction is not None
