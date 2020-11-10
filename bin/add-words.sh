#!/usr/bin/env bash

# db-update.sh - given a configured TSV file, update an SQLite database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 11, 2020 - first cut


# configure
TSV="./tmp/words.tsv"
DB='./etc/patents.db'
TABLE='words'
PATTERN='normalized-titles_'

cat ./tmp/$PATTERN* > $TSV

# do the work and done
echo "DELETE FROM $TABLE;" | sqlite3 $DB
echo -e ".mode tabs\n.import $TSV $TABLE" | sqlite3 $DB
exit
