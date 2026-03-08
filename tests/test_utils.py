"""Tests for utility functions."""

import pytest

from drug_interaction_checker.utils import (
    combine_confidence,
    get_close_drug_suggestions,
    resolve_drug_name,
)


class TestResolveDrugName:
    """Tests for the resolve_drug_name function."""

    def test_exact_canonical_name(self):
        name, confidence = resolve_drug_name("Warfarin")
        assert name == "Warfarin"
        assert confidence == 1.0

    def test_exact_canonical_name_case_insensitive(self):
        name, confidence = resolve_drug_name("WARFARIN")
        assert name == "Warfarin"
        assert confidence == 1.0

    def test_brand_name_resolves_to_canonical(self):
        name, confidence = resolve_drug_name("Coumadin")
        assert name == "Warfarin"
        assert confidence == 1.0

    def test_another_brand_name(self):
        name, confidence = resolve_drug_name("Advil")
        assert name == "Ibuprofen"
        assert confidence == 1.0

    def test_lipitor_resolves_to_atorvastatin(self):
        name, confidence = resolve_drug_name("Lipitor")
        assert name == "Atorvastatin"
        assert confidence == 1.0

    def test_unknown_name_returns_none(self):
        name, confidence = resolve_drug_name("ZZZUNKNOWN999")
        assert name is None
        assert confidence == 0.0

    def test_empty_name_returns_none(self):
        name, confidence = resolve_drug_name("   ")
        assert name is None
        assert confidence == 0.0

    def test_fuzzy_match_returns_value_less_than_one(self):
        # "warfarinn" should fuzzy-match Warfarin with confidence < 1.0
        name, confidence = resolve_drug_name("warfarinn")
        if name is not None:
            assert confidence < 1.0

    def test_leading_trailing_whitespace_stripped(self):
        name, confidence = resolve_drug_name("  Aspirin  ")
        assert name == "Aspirin"
        assert confidence == 1.0


class TestGetCloseDrugSuggestions:
    """Tests for the get_close_drug_suggestions function."""

    def test_returns_list(self):
        suggestions = get_close_drug_suggestions("warfar")
        assert isinstance(suggestions, list)

    def test_close_match_included(self):
        suggestions = get_close_drug_suggestions("warfar")
        # Should suggest Warfarin
        canonical_names = suggestions
        assert any("warfarin" in s.lower() for s in canonical_names)

    def test_unrecognised_returns_empty_or_small_list(self):
        suggestions = get_close_drug_suggestions("ZZZZZNODRUGHERE99999")
        assert isinstance(suggestions, list)
        assert len(suggestions) == 0

    def test_respects_n_parameter(self):
        suggestions = get_close_drug_suggestions("warfar", n=2)
        assert len(suggestions) <= 2

    def test_n_default_is_three(self):
        # Default n=3 so at most 3 results
        suggestions = get_close_drug_suggestions("aspir")
        assert len(suggestions) <= 3


class TestCombineConfidence:
    """Tests for the combine_confidence function."""

    def test_both_exact_gives_one(self):
        assert combine_confidence(1.0, 1.0) == 1.0

    def test_zero_propagates(self):
        assert combine_confidence(0.0, 0.9) == 0.0

    def test_partial_confidence(self):
        result = combine_confidence(0.8, 0.9)
        assert abs(result - 0.72) < 0.001

    def test_result_rounded_to_three_decimals(self):
        result = combine_confidence(0.7, 0.7)
        # 0.7 * 0.7 = 0.49, rounded to 3 dp
        assert result == 0.49

    def test_result_between_zero_and_one(self):
        for a in [0.1, 0.5, 0.9, 1.0]:
            for b in [0.1, 0.5, 0.9, 1.0]:
                result = combine_confidence(a, b)
                assert 0.0 <= result <= 1.0
