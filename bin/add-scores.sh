#!/usr/bin/env bash

# db-scores.sh - given a configured TSV file, update an SQLite database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 11, 2020 - first cut


# configure
TSV="./tmp/scores.tsv"
DB='./etc/patents.db'
TABLE='scores'


# do the work and done
echo "DELETE FROM $TABLE;" | sqlite3 $DB
echo -e ".mode tabs\n.import $TSV $TABLE" | sqlite3 $DB
exit
