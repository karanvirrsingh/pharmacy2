"""Tests for the drug interaction database."""

import pytest

from drug_interaction_checker.database import (
    ALIAS_MAP,
    ALL_DRUG_NAMES,
    DRUG_ALIASES,
    INTERACTION_MAP,
    _RAW_INTERACTIONS,
)
from drug_interaction_checker.models import Severity


class TestDrugAliases:
    """Tests for the DRUG_ALIASES registry."""

    def test_alias_map_contains_canonical_names(self):
        """Every Drug's primary name should appear in ALIAS_MAP."""
        for drug in DRUG_ALIASES:
            assert drug.name.lower() in ALIAS_MAP, (
                f"Canonical name '{drug.name}' not found in ALIAS_MAP"
            )

    def test_alias_map_contains_aliases(self):
        """Every alias in DRUG_ALIASES should appear in ALIAS_MAP."""
        for drug in DRUG_ALIASES:
            for alias in drug.aliases:
                assert alias.lower() in ALIAS_MAP, (
                    f"Alias '{alias}' for '{drug.name}' not found in ALIAS_MAP"
                )

    def test_alias_maps_to_correct_canonical(self):
        """Aliases must point back to the correct canonical drug name."""
        assert ALIAS_MAP.get("coumadin") == "Warfarin"
        assert ALIAS_MAP.get("advil") == "Ibuprofen"
        assert ALIAS_MAP.get("lipitor") == "Atorvastatin"
        assert ALIAS_MAP.get("plavix") == "Clopidogrel"

    def test_all_drug_names_is_sorted(self):
        """ALL_DRUG_NAMES should be a sorted list."""
        assert ALL_DRUG_NAMES == sorted(ALL_DRUG_NAMES)

    def test_at_least_50_drug_entries(self):
        """Database should have at least 50 drug aliases."""
        assert len(DRUG_ALIASES) >= 50


class TestInteractionMap:
    """Tests for the INTERACTION_MAP."""

    def test_at_least_30_interactions(self):
        """Database should contain at least 30 interaction entries."""
        assert len(INTERACTION_MAP) >= 30

    def test_known_interactions_present(self):
        """Spot-check that specific well-known interactions are in the map."""
        known_pairs = [
            ("warfarin", "aspirin"),
            ("warfarin", "metronidazole"),
            ("morphine", "alcohol"),
            ("phenelzine", "fluoxetine"),
            ("simvastatin", "clarithromycin"),
            ("metoprolol", "verapamil"),
            ("sildenafil", "nitroglycerin"),
        ]
        for d1, d2 in known_pairs:
            key = frozenset([d1, d2])
            assert key in INTERACTION_MAP, (
                f"Expected interaction ({d1} + {d2}) not found in INTERACTION_MAP"
            )

    def test_interaction_map_keys_are_frozensets(self):
        """All keys in INTERACTION_MAP must be frozensets."""
        for key in INTERACTION_MAP:
            assert isinstance(key, frozenset), f"Key {key!r} is not a frozenset"

    def test_interaction_map_values_are_interactions(self):
        """All values in INTERACTION_MAP must be Interaction instances."""
        from drug_interaction_checker.models import Interaction

        for value in INTERACTION_MAP.values():
            assert isinstance(value, Interaction)

    def test_severity_values_are_valid(self):
        """Every interaction should have a valid Severity value."""
        valid_severities = set(Severity)
        for interaction in _RAW_INTERACTIONS:
            assert interaction.severity in valid_severities, (
                f"Invalid severity '{interaction.severity}' for "
                f"{interaction.drug1} + {interaction.drug2}"
            )

    def test_interactions_have_non_empty_fields(self):
        """Description, mechanism, and recommendation must not be blank."""
        for interaction in _RAW_INTERACTIONS:
            pair = f"{interaction.drug1} + {interaction.drug2}"
            assert interaction.description.strip(), f"Empty description for {pair}"
            assert interaction.mechanism.strip(), f"Empty mechanism for {pair}"
            assert interaction.recommendation.strip(), f"Empty recommendation for {pair}"

    def test_all_severity_levels_represented(self):
        """The database should cover all four severity levels."""
        severities_used = {ix.severity for ix in _RAW_INTERACTIONS}
        for level in Severity:
            assert level in severities_used, (
                f"Severity '{level.value}' has no entries in the database"
            )

    def test_interaction_drug_pair_canonical_form(self):
        """drug_pair() should return a sorted tuple of lowercased names."""
        interaction = _RAW_INTERACTIONS[0]
        pair = interaction.drug_pair()
        assert len(pair) == 2
        assert pair == tuple(sorted([interaction.drug1.lower(), interaction.drug2.lower()]))
