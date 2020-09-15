

-- queries.sql - a set of SQL SELECT statements used to summarize the content of the given database

-- Eric Lease Morgan <emorgan@nd.edu>
-- (c) University of Notre Dame; distributed under a GNU Public License

-- September 15, 2020 - first cut


-- configure; tab'ed output so things can be copy & pasted into a spreadsheet for charting purposes
.mode tabs


-- introduction
SELECT "";
SELECT "Report";
SELECT "======";
SELECT "";
SELECT "The following is a simple report summarizing the contents of the given";
SELECT "database (./etc/patents.db). By reading the report you will garner an";
SELECT "understanding of the nature the collected patents. By studying the file";
SELECT "which created this report (./etc/queries.sql) you will begin to learn";
SELECT "how to use the Structured Query Language (SQL) to create your own";
SELECT "reports.";
SELECT "";
SELECT "Be forewarned. The database includes a complete list of patents, but";
SELECT "only a random sample of 10,000 records have been normalized and scored.";
SELECT "";
SELECT "                                                                     --";
SELECT "                                     Eric Lease Morgan <emorgan@nd.edu>";
SELECT "                                                     September 15, 2020";
SELECT "";



-- output the database's structure
SELECT "";
SELECT "";
SELECT "Database schema";
SELECT "---------------";
.schema


-- number of records
SELECT "";
SELECT "";
SELECT "Total number of records";
SELECT "-----------------------";
SELECT COUNT( id ) FROM titles;


-- number of records in each year
SELECT "";
SELECT "";
SELECT "Total number of records for each year; chart this to visualize 'inventiveness'.";
SELECT "-------------------------------------------------------------------------------";
SELECT year, COUNT( year ) FROM titles GROUP BY year ORDER BY year ASC;


-- number of duplicate titles
SELECT "";
SELECT "";
SELECT "List of top 10 duplicate titles; are we sure the original data is valid?";
SELECT "------------------------------------------------------------------------";
SELECT COUNT( id ) AS c, title FROM titles GROUP BY title ORDER BY c DESC LIMIT 10;


-- sample of a given duplicate title
SELECT "";
SELECT "";
SELECT "List of 10 patents with the title of 'Internal combustion engine'";
SELECT "-----------------------------------------------------------------";
SELECT * FROM titles WHERE title IS 'Internal combustion engine' ORDER BY year ASC LIMIT 10;


-- total number of unique patents
SELECT "";
SELECT "";
SELECT "Total number of 'unique' patents (scores = 0)";
SELECT "---------------------------------------------";
SELECT COUNT( id ) FROM scores WHERE score = 0;


-- total number of un-unique patents
SELECT "";
SELECT "";
SELECT "Total number of 'completely un-unique' patents (scores = 1)";
SELECT "-----------------------------------------------------------";
SELECT COUNT( id ) FROM scores WHERE score = 1;


-- least unique scores
SELECT "";
SELECT "";
SELECT "List of 25 LEAST unique scores and the number of patents with that score";
SELECT "------------------------------------------------------------------------";
SELECT score, COUNT( score ) FROM scores GROUP BY score ORDER BY score DESC LIMIT 25;


-- most unique scores
SELECT "";
SELECT "";
SELECT "List of 25 MOST unique scores and the number of patents with that score";
SELECT "-----------------------------------------------------------------------";
SELECT score, COUNT( score ) FROM scores GROUP BY score ORDER BY score ASC LIMIT 25;


-- least unique patents
SELECT "";
SELECT "";
SELECT "Random list of 10 'un-unique' patents with their identifiers and years";
SELECT "----------------------------------------------------------------------";
SELECT t.id, t.year, t.title FROM titles AS t, scores AS s WHERE s.score = 1 AND t.id = s.id ORDER BY RANDOM() LIMIT 10;


-- unique patents
SELECT "";
SELECT "";
SELECT "Random list of 10 'unique' patents with their identifiers and years";
SELECT "-------------------------------------------------------------------";
SELECT t.id, t.year, t.title FROM titles AS t, scores AS s WHERE s.score = 0 AND t.id = s.id ORDER BY RANDOM() LIMIT 10;


-- padding, just for fun
SELECT "";
SELECT "";


