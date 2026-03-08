"""Core drug interaction checking logic."""

from typing import Optional

from drug_interaction_checker.database import INTERACTION_MAP
from drug_interaction_checker.models import Interaction, InteractionResult
from drug_interaction_checker.utils import (
    combine_confidence,
    get_close_drug_suggestions,
    resolve_drug_name,
)


class DrugInteractionChecker:
    """AI-powered drug interaction checker backed by a curated knowledge base.

    Usage::

        checker = DrugInteractionChecker()
        result = checker.check("Warfarin", "Aspirin")
        if result.found:
            print(result.interaction.description)
    """

    def check(self, drug1_query: str, drug2_query: str) -> InteractionResult:
        """Check for an interaction between two drugs.

        Performs fuzzy name resolution followed by a knowledge-base lookup.

        Args:
            drug1_query: First drug name (generic, brand, or approximate spelling).
            drug2_query: Second drug name (generic, brand, or approximate spelling).

        Returns:
            An :class:`~drug_interaction_checker.models.InteractionResult`
            containing the matched names, interaction details (if found),
            confidence score, and a human-readable message.
        """
        drug1_canonical, conf1 = resolve_drug_name(drug1_query)
        drug2_canonical, conf2 = resolve_drug_name(drug2_query)

        result = InteractionResult(
            drug1_query=drug1_query,
            drug2_query=drug2_query,
            drug1_matched=drug1_canonical,
            drug2_matched=drug2_canonical,
        )

        # ── Unrecognised drug names ──────────────────────────────────────────
        if drug1_canonical is None:
            suggestions = get_close_drug_suggestions(drug1_query)
            suggestion_text = (
                f"  Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            )
            result.message = (
                f"Could not recognise drug '{drug1_query}'.{suggestion_text}"
            )
            return result

        if drug2_canonical is None:
            suggestions = get_close_drug_suggestions(drug2_query)
            suggestion_text = (
                f"  Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            )
            result.message = (
                f"Could not recognise drug '{drug2_query}'.{suggestion_text}"
            )
            return result

        # ── Same drug check ──────────────────────────────────────────────────
        if drug1_canonical.lower() == drug2_canonical.lower():
            result.message = (
                f"Both inputs resolve to the same drug ({drug1_canonical}). "
                "Please enter two different drugs."
            )
            return result

        # ── Interaction lookup ───────────────────────────────────────────────
        key = frozenset([drug1_canonical.lower(), drug2_canonical.lower()])
        interaction: Optional[Interaction] = INTERACTION_MAP.get(key)

        combined_confidence = combine_confidence(conf1, conf2)
        result.confidence = combined_confidence

        if interaction is not None:
            result.interaction = interaction
            match_note = self._match_note(drug1_query, drug1_canonical, conf1)
            match_note += self._match_note(drug2_query, drug2_canonical, conf2)
            result.message = (
                f"Interaction found between {drug1_canonical} and "
                f"{drug2_canonical}." + match_note
            )
        else:
            result.message = (
                f"No known interaction found between {drug1_canonical} and "
                f"{drug2_canonical} in the database.\n"
                "⚠️  This does not mean the combination is safe — always consult "
                "a healthcare professional or a comprehensive reference."
            )

        return result

    # ── private helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _match_note(query: str, canonical: str, confidence: float) -> str:
        """Return a note about fuzzy matching if the query differs from canonical."""
        if query.strip().lower() != canonical.lower() and confidence < 1.0:
            return (
                f"\n  ('{query}' matched to '{canonical}' with "
                f"{confidence * 100:.0f}% confidence)"
            )
        if query.strip().lower() != canonical.lower():
            return f"\n  ('{query}' resolved to '{canonical}')"
        return ""
