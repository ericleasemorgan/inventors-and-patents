#!/usr/bin/env bash

# split-words.sh - given a few configurations, create a set of files where each file contains words from a patent

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# November 6, 2020 - first cut


# configure
FILES=100
SQL=".mode tabs\nSELECT * FROM words ORDER BY year;"
DB='./etc/patents.db'
WORDS='words.tsv'
TMP='./tmp'
PREFIX='measure-inputs.'

# initialize; don't put things in tmp that you want to keep for very long
rm $TMP/*

# create a long list of records
echo -e "$SQL" | sqlite3 $DB > "$TMP/$WORDS"
COUNT=$( cat "$TMP/$WORDS" | wc -l )

# create a set of batches
cd $TMP
SIZE=$((($COUNT/$FILES)-1))
split --lines=$SIZE $WORDS $PREFIX

# done
exit
