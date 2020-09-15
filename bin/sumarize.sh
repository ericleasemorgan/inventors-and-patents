#!/usr/bin/env bash


# summarize.sh - given a set of SQL statements, output a report; a front-end to ./etc/queries.sql

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 15, 2020 - first cut


# configure
SQL='./etc/queries.sql'
DB='./etc/patents.db'

# do the work and done
cat $SQL | sqlite3 $DB
exit
