[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![Works with Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

# Taxonomy Update for LINNAEUS

This project contains the functions necessary to update the list of species used by LINNAEUS.

> Gerner, M.; Nenadic, G. & Bergman, C. M.
> LINNAEUS: A species name identification system for biomedical literature
> BMC Bioinformatics, 2010, 11, 85

------

The species dictionaries available for LINNAEUS via https://sourceforge.net/projects/linnaeus/files/Entity_packs/ haven't been updated since 2011. To be able to tag the most recently  discovered species, build a new one using the following simple steps:

```bash
git clone https://github.com/JULIELab/taxonupdate.git
cd taxonupdate
wget ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
# With default arguments, this is equal to:
# python DictWriter.py -i taxonomy.dat -o taxonomy.tsv --rank species
python DictWriter.py
```

Additionally, it is possible to restrict the dictionary to a subtree defined by its root ID.
E. g., if one wanted to only extract bacterial species, it can be done issuing:

```bash
python DictWriter -o bacterial_species.tsv --root 2
```

## List of major taxonomic groups

To make the use of this feature easier, it might help to consult the following lists:

### Superkingdoms

Archaea (ID: 2157)
Bacteria (ID: 2)
Eukaryota (ID: 2759)
Viroids (ID: 12884)
Viruses (ID: 10239)

### Kingdoms

Fungi (ID: 4751)
Metazoa (ID: 33208)
Viridiplantae (ID: 33090)

