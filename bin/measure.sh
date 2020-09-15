#!/usr/bin/env bash

# measure.sh - a front-end to measure.py

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 14, 2020 - first cut; needs to be submitted to the cluster


# configure
SQL=".mode tabs\nSELECT id, year, words FROM words limit 10000;"
DB='./etc/patents.db'
WORDS='./tmp/words.tsv'
SCORES='./tmp/scores.tsv'

echo -e "$SQL" | sqlite3 $DB > $WORDS
cat $WORDS | parallel ./bin/measure.py > $SCORES