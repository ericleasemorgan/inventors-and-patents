#!/usr/bin/env bash

# split-titles.sh - given a few configurations, create a set of files where each file contains a patent title

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 14, 2020 - first cut; ought to be submitted to the cluster
# October   15, 2020 - creates a set of files to process


# configure
FILES=100
SQL=".mode tabs\nSELECT id, year, title FROM titles ORDER BY year;"
DB='./etc/patents.db'
TITLES='titles.tsv'
TMP='./tmp'
PREFIX='title-inputs.'

# initialize; don't put things in tmp that you want to keep for very long
rm $TMP/*

# create a long list of records
echo -e "$SQL" | sqlite3 $DB > "$TMP/$TITLES"
COUNT=$( cat "$TMP/$TITLES" | wc -l )

# create a set of batches
cd $TMP
SIZE=$((($COUNT/$FILES)-1))
split --lines=$SIZE $TITLES $PREFIX

# done
exit
