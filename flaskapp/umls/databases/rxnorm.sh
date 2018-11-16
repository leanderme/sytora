#!/bin/sh
#
#  create an RxNORM SQLite database (and a relations triple store).
#

# our SQLite database does not exist
if [ ! -e rxnorm.db ]; then
	if [ ! -d "$1" ]; then
		echo "Provide the path to the RxNorm directory as first argument when invoking this script. Download the latest version here: http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"
		exit 1
	fi
	if [ ! -d "$1/rrf" ]; then
		echo "There is no directory named rrf in the directory you provided. Download the latest version here: http://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"
		exit 1
	fi
	if ! hash sqlite3 &>/dev/null; then
		echo "It seems 'sqlite3' is not installed, I will need it. Aborting."
		exit 1
	fi
	
	# init the database
	cat "$1/scripts/mysql/Table_scripts_mysql_rxn.sql" | sqlite3 rxnorm.db
	
	# convert RRF files (strip last pipe and remove quote (") characters, those are giving SQLite troubles)
	if [ ! -e "$1/rrf/RXNREL.pipe" ]; then
		current=$(pwd)
		cd "$1/rrf"
		echo "->  Converting RRF files for SQLite"
		for f in *.RRF; do
			sed -e 's/.$//' -e 's/"//g' "$f" > "${f%RRF}pipe"
		done
		cd $current
	fi
	
	# import tables
	for f in "$1/rrf/"*.pipe; do
		table=$(basename ${f%.pipe})
		echo "->  Importing $table"
		sqlite3 rxnorm.db ".import '$f' '$table'"
	done
	
	# create an NDC table
	echo "->  Creating extra tables"
	# sqlite3 rxnorm.db "CREATE TABLE NDC AS SELECT RXCUI, ATV AS NDC FROM RXNSAT WHERE ATN = 'NDC';"	# we do it in 2 steps to create the primary index column
	sqlite3 rxnorm.db "CREATE TABLE NDC (RXCUI INT, NDC VARCHAR);"
	sqlite3 rxnorm.db "INSERT INTO NDC SELECT RXCUI, ATV FROM RXNSAT WHERE ATN = 'NDC';"
	
	# create drug class tables
	sqlite3 rxnorm.db "CREATE TABLE VA_DRUG_CLASS (RXCUI int, RXCUI_ORIGINAL int, VA varchar);"
	sqlite3 rxnorm.db "CREATE TABLE FRIENDLY_CLASS_NAMES (VACODE varchar, FRIENDLY varchar);"
	sqlite3 rxnorm.db "CREATE INDEX X_FRIENDLY_CLASS_NAMES_VACODE ON FRIENDLY_CLASS_NAMES (VACODE);"
	
	# create indices
	echo "->  Indexing NDC table"
	sqlite3 rxnorm.db "CREATE INDEX X_NDC_RXCUI ON NDC (RXCUI);"
	sqlite3 rxnorm.db "CREATE INDEX X_NDC_NDC ON NDC (NDC);"
	
	echo "->  Indexing RXNSAT table"
	sqlite3 rxnorm.db "CREATE INDEX RXNSAT_RXCUI ON RXNSAT (RXCUI);"
	sqlite3 rxnorm.db "CREATE INDEX RXNSAT_ATN ON RXNSAT (ATN);"
	
	echo "->  Indexing RXNREL table"
	sqlite3 rxnorm.db "CREATE INDEX X_RXNREL_RXCUI1 ON RXNREL (RXCUI1);"
	sqlite3 rxnorm.db "CREATE INDEX X_RXNREL_RXCUI2 ON RXNREL (RXCUI2);"
	sqlite3 rxnorm.db "CREATE INDEX X_RXNREL_RXAUI2 ON RXNREL (RXAUI2);"
	#sqlite3 rxnorm.db "CREATE INDEX X_RXNREL_RELA ON RXNREL (RELA);"		# do NOT do this! slows down queries dramatically
	
	echo "->  Indexing RXNCONSO table"
	sqlite3 rxnorm.db "CREATE INDEX X_RXNCONSO_RXCUI ON RXNCONSO (RXCUI);"
	sqlite3 rxnorm.db "CREATE INDEX X_RXNCONSO_RXAUI ON RXNCONSO (RXAUI);"
	
	# How to export from SQLite: export NDC to CSV
	# .mode csv
	# .header on
	# .out va-class.csv
	# SELECT RXCUI, NDC FROM NDC;
	# SELECT DISTINCT ATV FROM RXNSAT WHERE ATN = 'VA_CLASS_NAME' ORDER BY ATV ASC;
fi

