"""Utility functions for drug name matching and result formatting."""

import difflib
from typing import Optional, Tuple

from drug_interaction_checker.database import ALIAS_MAP, ALL_DRUG_NAMES


# ---------------------------------------------------------------------------
# Name matching
# ---------------------------------------------------------------------------

_MATCH_CUTOFF = 0.6  # minimum similarity score to accept a fuzzy match


def resolve_drug_name(query: str) -> Tuple[Optional[str], float]:
    """Resolve a user-supplied drug name to a canonical drug name.

    Performs an exact lookup first, then falls back to fuzzy matching.

    Args:
        query: The drug name as entered by the user.

    Returns:
        A ``(canonical_name, confidence)`` tuple where *canonical_name* is
        ``None`` when no acceptable match was found.
    """
    normalised = query.strip().lower()

    # 1. Exact match (handles canonical names and aliases directly)
    if normalised in ALIAS_MAP:
        return ALIAS_MAP[normalised], 1.0

    # 2. Fuzzy match against the full alias list
    matches = difflib.get_close_matches(
        normalised,
        ALL_DRUG_NAMES,
        n=1,
        cutoff=_MATCH_CUTOFF,
    )
    if matches:
        best = matches[0]
        score = difflib.SequenceMatcher(None, normalised, best).ratio()
        canonical = ALIAS_MAP[best]
        return canonical, round(score, 3)

    return None, 0.0


def get_close_drug_suggestions(query: str, n: int = 3) -> list:
    """Return up to *n* suggested drug names for a given query string.

    Args:
        query: The drug name fragment or misspelling entered by the user.
        n: Maximum number of suggestions to return.

    Returns:
        A list of canonical drug name strings.
    """
    normalised = query.strip().lower()
    matches = difflib.get_close_matches(
        normalised,
        ALL_DRUG_NAMES,
        n=n,
        cutoff=0.4,
    )
    return [ALIAS_MAP[m] for m in matches]


# ---------------------------------------------------------------------------
# Confidence helpers
# ---------------------------------------------------------------------------

def combine_confidence(c1: float, c2: float) -> float:
    """Return the joint confidence of two independent name matches.

    Args:
        c1: Confidence for the first drug match (0–1).
        c2: Confidence for the second drug match (0–1).

    Returns:
        Combined confidence score (product, rounded to 3 d.p.).
    """
    return round(c1 * c2, 3)
