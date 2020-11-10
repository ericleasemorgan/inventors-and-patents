#!/afs/crc.nd.edu/user/e/emorgan//local/anaconda/bin/python

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

# sanity check
if len( sys.argv ) != 2 :
	sys.stderr.write( 'Usage: ' + sys.argv[ 0 ] + " <file>\n" )
	exit()

# get input
file = sys.argv[ 1 ]

# initialize database connection
connection = sqlite3.connect( DB )
cursor     = connection.cursor()

# open the given file
with open ( file ) as handle :

	# initialize
	record = handle.readline()
	record = record.rstrip()

	# process the record
	while record :
	
		# get the input and parse it
		fields = record.split( '\t' )
		key    = fields[ 0 ]
		year   = fields[ 1 ]
		words  = fields[ 2 ].split()


		# initialize scoring
		sum = 0
		total = len( words )

		# process each word
		for word in words :

			# get the number of times the word was previously used
			cursor.execute( SQL % ( word, year ) )
			count = cursor.fetchone()[ 0 ]
	
			# update the sum, conditionally
			if count > 0 : sum = sum + 1

			# debug
			#print( "\t".join( ( str( count ), word, str( sum ) ) ) )
	
		# calculate uniqueness
		uniqueness = sum / total

		# output and done
		print( "\t".join( ( str( key ), str( year ), str( uniqueness ) ) ) )

		# initialize
		record = handle.readline()
		record = record.rstrip()


# done
exit


