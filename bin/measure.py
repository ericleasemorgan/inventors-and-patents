#!/usr/bin/env python

# measure.py - given the words from a patent title, calculate a uniqueness score

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 14, 2020 - first cut


# configure
DB = './etc/patents.db'
SQL = "SELECT COUNT( id ) FROM words WHERE words LIKE '%%%s%%' AND year < '%s'"

# require
import sqlite3
import sys

# get the input and parse it
fields = sys.argv[ 1 ].split( '\t' )
key    = fields[ 0 ]
year   = fields[ 1 ]
words  = fields[ 2 ].split()

# initialize database connection
connection = sqlite3.connect( DB )
cursor     = connection.cursor()

# initialize scoring
sum = 0
total = len( words )

# process each word
for word in words :

	# get the number of times the word was previously used
	cursor.execute( SQL % ( word, year ) )
	count = cursor.fetchone()[ 0 ]
	
	# debug
	#print( "\t".join( ( str( count ), word ) ) )
	
	# update the sum, conditionally
	if count > 0 : sum = sum + 1

# calculate uniqueness
uniqueness = sum / total

# output and done
print( "\t".join( ( str( key ), str( year ), str( uniqueness ) ) ) )
exit


