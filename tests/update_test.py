#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the taxonomy updater."""

from typing import cast

from taxonomy_update import make_variants, taxonomy2dict
from DictWriter import DictWriter


def test_allalpha():
    """Only the scientific name should get variants."""
    strawberry = {
        "ID": "57918",
        "RANK": "species",
        "SCIENTIFIC NAME": ["Fragaria vesca"],
        "GENBANK COMMON NAME": ["wild strawberry"],
        "COMMON NAME": ["European strawberry", "alpine strawberry", "wood strawberry"],
    }
    expected = (
        "Alpine strawberry|European strawberry|F. vesca|F.vesca|"
        "Fragaria vesca|Wild strawberry|Wood strawberry|"
        "alpine strawberry|f. vesca|f.vesca|fragaria vesca|"
        "wild strawberry|wood strawberry"
    )
    variants = sorted(make_variants(strawberry))
    variants = "|".join(variants)

    assert variants == expected


def test_nonalpha():
    """The scientific name contains a dot, which should lead to
    no abbreviation for it."""
    sp301 = {"ID": "352854", "RANK": "species", "SCIENTIFIC NAME": ["Fragaria sp. 301"]}
    expected = "Fragaria sp. 301"
    variants = sorted(make_variants(sp301))
    variants = "|".join(variants)

    assert variants == expected


def test_create_dict():
    """The number of entries in the dictionary is 45."""
    expected = 45
    i = 0
    for _ in taxonomy2dict("tests/tax-test.dat"):
        i += 1

    assert i == expected


def test_species_entries():
    """The number of species entries in the dictionary is 18."""
    expected = 18
    i = 0
    for entry in taxonomy2dict("tests/tax-test.dat"):
        if entry["RANK"] == "species":
            i += 1

    assert i == expected


def test_subtree_filter_all():
    """The number of species entries in the dictionary is 18."""
    expected = 18
    writer = DictWriter()
    i = 0
    taxa = dict()
    for entry in taxonomy2dict("tests/tax-test.dat"):
        taxa[cast(str, entry["ID"])] = entry
    for entry in writer.filter_by_root(taxa, "1", "species"):
        i += 1
    assert i == expected


def test_subtree_filter_phylum():
    """There are 2 phyla in the dictionary. One is in the right subtree."""
    expected = 1
    writer = DictWriter()
    i = 0
    taxa = dict()
    for entry in taxonomy2dict("tests/tax-test.dat"):
        taxa[cast(str, entry["ID"])] = entry
    phyla = []
    for entry in writer.filter_by_root(taxa, "2", "phylum"):
        phyla.append(entry["SCIENTIFIC NAME"])
    assert len(phyla) == expected
    assert phyla[0] == ["Proteobacteria"]
