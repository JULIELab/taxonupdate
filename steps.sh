#!/usr/bin/env bash
git clone https://github.com/JULIELab/taxonupdate.git
cd taxonupdate
wget ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
# With default arguments, this is equal to:
# python DictWriter.py -i taxonomy.dat -o taxonomy.tsv --rank species
python DictWriter.py

