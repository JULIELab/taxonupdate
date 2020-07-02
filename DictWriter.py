#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line tool to easily generate updated dictionaries out of the NCBI Taxonomy.

Created on Fri Jun 12 11:12:11 2020

@author: Kampe
"""
import argparse
from typing import cast, Union
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
            The root of a subtree. Only entries from this subtree will be selected

        Returns
        -------
        int
            Number of lines (entries) written.

        """
        counter = 0
        if root:
            taxa = dict()
            for entry in taxonomy2dict(input):
                taxa[entry["ID"]] = entry
            with open(output, "wt") as out:
                for key, entry in taxa.items():
                    parent = entry["PARENT ID"]
                    while True:
                        if key == root:
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
                        else:
                            temp = taxa.get(parent, None)
                            if temp is None:
                                break
                            key = cast(str, temp["ID"])
                            parent = temp["PARENT ID"]
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
        help="Limit the selection to the subtree with this root, e.g. 'bacteria'",
        default="",
        type=str,
    )
    ARGS = PARSER.parse_args()
    input = Path(ARGS.input)
    if not input.exists():
        print(f"ERROR: Input file {input} does not exists.", file=sys.stderr)
        sys.exit(1)
    if not input.is_file():
        print(f"ERROR: Input argument {input} is not a file.", file=sys.stderr)
        sys.exit(1)
    output = Path(ARGS.output)
    if output.exists():
        print(f"ERROR: Output file {output} already exists.", file=sys.stdout)
        sys.exit(1)
    writer = DictWriter()
    lines = writer.write(ARGS.input, ARGS.output, ARGS.rank, ARGS.root)
    if lines == 1:
        print("Wrote 1 entry", file=sys.stdout)
    else:
        print(f"Wrote {lines} entries", file=sys.stdout)
