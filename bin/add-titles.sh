#!/usr/bin/env bash

# db-create.sh - given a configured CSV file, create an SQLite database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 11, 2020 - first cut


# configure
CSV="./etc/patents.csv"
DB='./etc/patents.db'
SCHEMA='./etc/schema.sql'
TABLE='titles'

# initialize
rm -rf $DB
cat $SCHEMA | sqlite3 $DB

# do the work and done
echo -e ".mode csv\n.import $CSV $TABLE" | sqlite3 $DB
exit
