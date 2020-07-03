#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line tool to easily generate updated dictionaries out of the NCBI Taxonomy.

Created on Fri Jun 12 11:12:11 2020

@author: Kampe
"""
import argparse
from typing import cast, Dict, Iterator, List, Union
from pathlib import Path
import sys
from taxonomy_update import make_variants, taxonomy2dict


class DictWriter:
    """All necessary functions to filter and write NCBI Taxonomy entries."""

    PREFIX = "species:ncbi:"

    RANKS = [
        "class",
        "cohort",
        "family",
        "forma",
        "genus",
        "infraclass",
        "infraorder",
        "kingdom",
        "no rank",
        "order",
        "parvorder",
        "phylum",
        "species",
        "species group",
        "species subgroup",
        "subclass",
        "subcohort",
        "subfamily",
        "subgenus",
        "subkingdom",
        "suborder",
        "subphylum",
        "subspecies",
        "subtribe",
        "superclass",
        "superfamily",
        "superkingdom",
        "superorder",
        "superphylum",
        "tribe",
        "varietas",
    ]

    def filter_by_root(
        self, taxa: Dict[str, Dict[str, Union[str, List[str]]]], root: str, rank: str
    ) -> Iterator[Dict[str, Union[str, List[str]]]]:
        """
        Filter all entries to restrict matches to a given subtree defined by the root.

        Parameters
        ----------
        taxa : Dict[str, Dict[str, Union[str, List[str]]]]
            A dictionary of NCBI Taxonomy entries
        root : str
            The root of a subtree. Only entries from this subtree will be selected
        rank : str
            Rank of the entry, e.g. 'species' or 'genus'

        Yields
        ------
        Iterator[Dict[str, Union[str, List[str]]]]
            Entries that are taxonomically below or equal to the root.

        """
        for key, entry in taxa.items():
            parent = cast(str, entry["PARENT ID"])
            while True:
                if key == root:
                    if entry["RANK"] == rank:
                        yield entry
                    break
                temp = taxa.get(parent, None)
                if temp is None:
                    break
                key = cast(str, temp["ID"])
                parent = cast(str, temp["PARENT ID"])

    def write(
        self, input: Union[Path, str], output: Union[Path, str], rank: str, root: str
    ) -> int:
        """
        Write a dictionary containing all entries of a specific rank.

        Parameters
        ----------
        input : Union[Path, str]
            Path to taxonomy.dat
        output : Union[Path, str]
            Write into this file
        rank : str
            Rank of the entry, e.g. 'species' or 'genus'
        root : str
            The root of a subtree. Only entries from this subtree will be selected.
            Corresponds to the ID of an entry.

        Returns
        -------
        int
            Number of lines (entries) written.

        """
        counter = 0
        if root:
            taxa: Dict[str, Dict[str, Union[str, List[str]]]] = dict()
            for entry in taxonomy2dict(input):
                taxa[cast(str, entry["ID"])] = entry
            with open(output, "wt") as out:
                for subtree_entry in self.filter_by_root(taxa, root, rank):
                    variants = sorted(make_variants(subtree_entry))
                    _ = out.write(
                        DictWriter.PREFIX
                        + cast(str, subtree_entry["ID"])
                        + "\t"
                        + "|".join(variants)
                        + "\n"
                    )
                    counter += 1
        else:
            with open(output, "wt") as out:
                for entry in taxonomy2dict(input):
                    if entry["RANK"] != rank:
                        continue
                    variants = sorted(make_variants(entry))
                    _ = out.write(
                        DictWriter.PREFIX
                        + cast(str, entry["ID"])
                        + "\t"
                        + "|".join(variants)
                        + "\n"
                    )
                    counter += 1
        return counter


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Writes a dictionary containing all entries of a specific rank"
    )
    PARSER.add_argument(
        "-r",
        "--rank",
        choices=DictWriter.RANKS,
        help="Rank of the entry",
        default="species",
        type=str,
    )
    PARSER.add_argument(
        "-i,",
        "--input",
        help="Path to taxonomy.dat",
        default="./taxonomy.dat",
        type=str,
    )
    PARSER.add_argument(
        "-o",
        "--output",
        help="Write into this file",
        default="./taxonomy.tsv",
        type=str,
    )
    PARSER.add_argument(
        "--root",
        help="Limit the selection to the subtree with this root, e.g. --root 2 (ID of bacteria superkingdom)'",
        default="",
        type=str,
    )
    ARGS = PARSER.parse_args()
    INPUT = Path(ARGS.input)
    if not INPUT.exists():
        print(f"ERROR: Input file {INPUT} does not exists.", file=sys.stderr)
        sys.exit(1)
    if not INPUT.is_file():
        print(f"ERROR: Input argument {INPUT} is not a file.", file=sys.stderr)
        sys.exit(1)
    OUTPUT = Path(ARGS.output)
    if OUTPUT.exists():
        print(f"ERROR: Output file {OUTPUT} already exists.", file=sys.stdout)
        sys.exit(1)
    WRITER = DictWriter()
    LINES = WRITER.write(ARGS.input, ARGS.output, ARGS.rank, ARGS.root)
    if LINES == 1:
        print("Wrote 1 entry", file=sys.stdout)
    else:
        print(f"Wrote {LINES} entries", file=sys.stdout)
