#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:12:11 2020

@author: Kampe
"""
import argparse
from typing import Union
import logging
from pathlib import Path
import sys
from taxonomy_update import make_variants, taxonomy2dict


class DictWriter:
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
        self, input: Union[Path, str], output: Union[Path, str], rank: str
    ) -> int:
        counter = 0
        with open(output, "wt") as out:
            for entry in taxonomy2dict(input):
                if entry["RANK"] != rank:
                    continue
                variants = sorted(make_variants(entry))
                _ = out.write(
                    DictWriter.PREFIX + entry["ID"] + "\t" + "|".join(variants) + "\n"
                )
                counter += 1
        return counter


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s")
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
    ARGS = PARSER.parse_args()
    input = Path(ARGS.input)
    if not input.exists():
        logging.error("Input file %s does not exists.", input)
        sys.exit(1)
    if not input.is_file():
        logging.error("Input argument %s is not a file.", input)
        sys.exit(1)
    output = Path(ARGS.output)
    if output.exists():
        logging.error("Output file %s already exists.", output)
        sys.exit(1)
    writer = DictWriter()
    lines = writer.write(ARGS.input, ARGS.output, ARGS.rank)
    logging.info("%d lines written", lines)
