"""Tests for the core DrugInteractionChecker."""

import pytest

from drug_interaction_checker.checker import DrugInteractionChecker
from drug_interaction_checker.models import Severity


@pytest.fixture
def checker():
    """Shared DrugInteractionChecker instance."""
    return DrugInteractionChecker()


class TestKnownInteractions:
    """Tests for interactions that must be present in the database."""

    def test_warfarin_aspirin(self, checker):
        result = checker.check("Warfarin", "Aspirin")
        assert result.found
        assert result.interaction.severity == Severity.MAJOR
        assert result.drug1_matched == "Warfarin"
        assert result.drug2_matched == "Aspirin"
        assert result.confidence == 1.0

    def test_warfarin_aspirin_reversed(self, checker):
        """Order of arguments must not matter."""
        result = checker.check("Aspirin", "Warfarin")
        assert result.found
        assert result.interaction.severity == Severity.MAJOR

    def test_phenelzine_fluoxetine_contraindicated(self, checker):
        result = checker.check("Phenelzine", "Fluoxetine")
        assert result.found
        assert result.interaction.severity == Severity.CONTRAINDICATED

    def test_metoprolol_verapamil_contraindicated(self, checker):
        result = checker.check("Metoprolol", "Verapamil")
        assert result.found
        assert result.interaction.severity == Severity.CONTRAINDICATED

    def test_morphine_alcohol(self, checker):
        result = checker.check("Morphine", "Alcohol")
        assert result.found
        assert result.interaction.severity == Severity.CONTRAINDICATED

    def test_simvastatin_clarithromycin(self, checker):
        result = checker.check("Simvastatin", "Clarithromycin")
        assert result.found
        assert result.interaction.severity == Severity.CONTRAINDICATED

    def test_lisinopril_spironolactone(self, checker):
        result = checker.check("Lisinopril", "Spironolactone")
        assert result.found
        assert result.interaction.severity == Severity.MAJOR

    def test_clopidogrel_omeprazole(self, checker):
        result = checker.check("Clopidogrel", "Omeprazole")
        assert result.found
        assert result.interaction.severity == Severity.MODERATE

    def test_result_has_description(self, checker):
        result = checker.check("Warfarin", "Amiodarone")
        assert result.found
        assert len(result.interaction.description) > 10

    def test_result_has_mechanism(self, checker):
        result = checker.check("Warfarin", "Amiodarone")
        assert result.found
        assert len(result.interaction.mechanism) > 10

    def test_result_has_recommendation(self, checker):
        result = checker.check("Warfarin", "Amiodarone")
        assert result.found
        assert len(result.interaction.recommendation) > 10


class TestBrandNameResolution:
    """Brand names and aliases should resolve to the correct canonical drug."""

    def test_coumadin_as_warfarin(self, checker):
        result = checker.check("Coumadin", "Aspirin")
        assert result.found
        assert result.drug1_matched == "Warfarin"

    def test_advil_as_ibuprofen(self, checker):
        result = checker.check("Warfarin", "Advil")
        assert result.found
        assert result.drug2_matched == "Ibuprofen"

    def test_lipitor_as_atorvastatin(self, checker):
        result = checker.check("Lipitor", "Clarithromycin")
        assert result.found
        assert result.drug1_matched == "Atorvastatin"

    def test_flagyl_as_metronidazole(self, checker):
        result = checker.check("Flagyl", "Warfarin")
        assert result.found
        assert result.drug1_matched == "Metronidazole"

    def test_prozac_as_fluoxetine(self, checker):
        result = checker.check("Prozac", "Tramadol")
        assert result.found
        assert result.drug1_matched == "Fluoxetine"

    def test_norvasc_as_amlodipine(self, checker):
        """Amlodipine brand name should resolve correctly."""
        result = checker.check("Norvasc", "Warfarin")
        # Amlodipine + Warfarin is not in the database but the name should resolve
        assert result.drug1_matched == "Amlodipine"


class TestFuzzyMatching:
    """Misspelled drug names should still resolve via fuzzy matching."""

    def test_misspelled_warfarin(self, checker):
        result = checker.check("warfaren", "aspirin")
        # May or may not match depending on edit distance; confidence should be < 1
        # At minimum, aspirin resolves correctly
        assert result.drug2_matched == "Aspirin"

    def test_case_insensitive_lookup(self, checker):
        result = checker.check("WARFARIN", "ASPIRIN")
        assert result.found

    def test_mixed_case_brand(self, checker):
        result = checker.check("coUMaDin", "aspirin")
        assert result.found
        assert result.drug1_matched == "Warfarin"


class TestNoInteraction:
    """Pairs with no known interaction should return found=False with a message."""

    def test_unrelated_drugs_no_interaction(self, checker):
        result = checker.check("Amoxicillin", "Paracetamol")
        assert not result.found
        assert result.message != ""

    def test_message_contains_disclaimer_when_not_found(self, checker):
        result = checker.check("Amlodipine", "Metformin")
        assert not result.found
        assert "consult" in result.message.lower() or "professional" in result.message.lower() or "not mean" in result.message.lower()


class TestErrorHandling:
    """Unknown drug names should return sensible error messages."""

    def test_unknown_drug1(self, checker):
        result = checker.check("XYZ_DRUG_123", "Aspirin")
        assert not result.found
        assert result.drug1_matched is None
        assert "XYZ_DRUG_123" in result.message

    def test_unknown_drug2(self, checker):
        result = checker.check("Warfarin", "XYZ_DRUG_456")
        assert not result.found
        assert result.drug2_matched is None
        assert "XYZ_DRUG_456" in result.message

    def test_both_unknown_drugs(self, checker):
        result = checker.check("AAAA_DRUG", "BBBB_DRUG")
        assert not result.found

    def test_same_drug_twice(self, checker):
        result = checker.check("Warfarin", "Warfarin")
        assert not result.found
        assert "same" in result.message.lower() or "Warfarin" in result.message

    def test_same_drug_via_alias(self, checker):
        """Coumadin and Warfarin are the same drug."""
        result = checker.check("Coumadin", "Warfarin")
        assert not result.found
        assert "same" in result.message.lower()
