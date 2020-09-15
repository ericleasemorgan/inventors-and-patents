#!/usr/bin/env bash

# normalize.sh - a front-end to normalize.py

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 14, 2020 - first cut; ought to be submitted to the cluster


# configure
SQL=".mode tabs\nSELECT id, year, title FROM titles ORDER BY RANDOM() ASC limit 100000;"
DB='./etc/patents.db'
TITLES='./tmp/titles.tsv'
WORDS='./tmp/words.tsv'

echo -e "$SQL" | sqlite3 $DB > $TITLES
cat $TITLES | parallel ./bin/normalize.py > $WORDS