Taxonomy Update for LINNAEUS
============================

This project contains the functions necessary to update the list of species used by LINNAEUS.

  Gerner, M.; Nenadic, G. & Bergman, C. M.
  LINNAEUS: A species name identification system for biomedical literature
  BMC Bioinformatics, 2010, 11, 85

---------------

The species dictionaries available for LINNAEUS via https://sourceforge.net/projects/linnaeus/files/Entity_packs/ haven't been updated since 2011. To be able to tag the most recently discovered species, build a new one using the following lines of Python::

  from taxonomy_update import make_variants, taxonomy2dict

  PREFIX = 'species:ncbi:'
  tax = 'taxonomy.dat'
  with open('dict-species.tsv', 'wt') as species:
      for entry in taxonomy2dict(tax):
          if entry['RANK'] != 'species':
              continue
          variants = sorted(make_variants(entry))
          species.write(PREFIX + entry['ID'] + '\t' + '|'.join(variants) + '\n')

taxonomy.dat can be downloaded from ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
