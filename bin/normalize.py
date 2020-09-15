#!/usr/bin/env python

# normalize.py - given a line, output text which has been cleaned

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# September 11, 2020 - first cut


# configure
STOPWORDS = './etc/stop-words.txt'

# require
import sys, re, string

# initialize stop words and translation table
stopwords = open( STOPWORDS ).read().split( '\n' )
table     = str.maketrans( '', '', string.punctuation )

# normalization process; the hard work gets done here
def normalize( words ) :

	# lowercase and parse
	words = words.lower().split()
	
	# remove stop words, digits, and punctuation
	words = [ word for word in words if word not in stopwords ]
	words = [ ( re.sub( '\d+', '', word ) ) for word in words ]
	words = [ word.translate( table ) for word in words ]
	
	# re-join and done
	return ' '.join( words )

# get the input and parse it
fields = sys.argv[ 1 ].split( '\t' )
key    = fields[ 0 ]
year   = fields[ 1 ]
title  = fields[ 2 ]

# do the work, output, and done
words = normalize( title )
print( "\t".join( ( key, year, words ) ) )
exit
