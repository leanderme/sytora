#!/bin/sh
#
#  create a UMLS SQLite database.
#

# our SQLite database does not exist
if [ ! -e umls.db ]; then
	if [ ! -d "$1" ]; then
		echo "Provide the path to the UMLS install directory, which is named something like \"2014AA\" and contains a \"META\" directory, as first argument when invoking this script."
		echo
		echo "Downloading and Extracting UMLS Data"
		echo "===================================="
		echo
		echo "Downloading and extracting UMLS data is a painful process."
		echo "Begin by downloading most files for the latest version listed on the left side here: http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html"
		echo "Extract 'mmsys.zip' and place every downloaded file, including 'mmsys.zip', into the extracted directory."
		echo "Run the respective 'runXX' script inside the mmsys directory; the MetamorphoSys Java GUI will open."
		echo "Click \"Install UMLS\", as source directory select the just extracted mmsys directory and your chosen target directory."
		echo "Leave the checkboxes alone and click OK."
		echo "Now you must generate a configuration and in order to be able to proceed, save the configuration via a command from the menu bar."
		echo "Then select \"Begin Subset\", also from the menubar, to start the extraction process."
		echo "This should extract all the things and put in in the selected directory, which now contains a META directory with all the files we need to proceed."
		echo
		echo "Once you have done this, run this script again with the correct path as the first argument."
		exit 1
	fi
	if [ ! -d "$1/META" ]; then
		echo "There is no directory named META in the install directory you provided."
		echo "Point this script to the directory named something like \"2014AA\"."
		exit 1
	fi
	
	# convert RRF files (strip last pipe and remove quote (") characters, those are giving SQLite troubles)
	if [ ! -e "$1/META/MRDEF.pipe" ]; then
		current=$(pwd)
		cd "$1/META"
		echo "-> Converting RRF files for SQLite"
		for f in MRCONSO.RRF MRDEF.RRF MRSTY.RRF; do
			sed -e 's/.$//' -e 's/"//g' "$f" > "${f%RRF}pipe"
		done
		cd $current
	fi
	
	# init the database for MRDEF
	# table structure here: http://www.ncbi.nlm.nih.gov/books/NBK9685/
	sqlite3 umls.db "CREATE TABLE MRDEF (
		CUI varchar,
		AUI varchar,
		ATUI varchar,
		SATUI varchar,
		SAB varchar,
		DEF text,
		SUPPRESS varchar,
		CVF varchar
	)"
	
	# init the database for MRCONSO
	sqlite3 umls.db "CREATE TABLE MRCONSO (
		CUI varchar,
		LAT varchar,
		TS varchar,
		LUI varchar,
		STT varchar,
		SUI varchar,
		ISPREF varchar,
		AUI varchar,
		SAUI varchar,
		SCUI varchar,
		SDUI varchar,
		SAB varchar,
		TTY varchar,
		CODE varchar,
		STR text,
		SRL varchar,
		SUPPRESS varchar,
		CVF varchar
	)"
	
	# init the database for MRSTY
	sqlite3 umls.db "CREATE TABLE MRSTY (
		CUI varchar,
		TUI varchar,
		STN varchar,
		STY text,
		ATUI varchar,
		CVF varchar
	)"
	
	# import tables
	for f in "$1/META/"*.pipe; do
		table=$(basename ${f%.pipe})
		echo "-> Importing $table"
		sqlite3 umls.db ".import '$f' '$table'"
	done
	
	# create indexes
	echo "-> Creating indexes"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRDEF ON MRDEF (CUI);"
	sqlite3 umls.db "CREATE INDEX X_SAB_MRDEF ON MRDEF (SAB);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRCONSO ON MRCONSO (CUI);" 
	sqlite3 umls.db "CREATE INDEX X_LAT_MRCONSO ON MRCONSO (LAT);"
	sqlite3 umls.db "CREATE INDEX X_TS_MRCONSO ON MRCONSO (TS);"
	sqlite3 umls.db "CREATE INDEX X_CUI_MRSTY ON MRSTY (CUI);"
	sqlite3 umls.db "CREATE INDEX X_TUI_MRSTY ON MRSTY (TUI);"
	
	# create faster lookup table
	# LAT codes https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html
	echo "-> Creating fast lookup table"
	sqlite3 umls.db "CREATE TABLE descriptions AS SELECT CUI, LAT, SAB, TTY, STR FROM MRCONSO WHERE LAT = 'ENG' OR LAT = 'GER' AND TS = 'P' AND ISPREF = 'Y'"
	sqlite3 umls.db "ALTER TABLE descriptions ADD COLUMN STY TEXT"
	sqlite3 umls.db "CREATE INDEX X_CUI_desc ON descriptions (CUI)"
	sqlite3 umls.db "UPDATE descriptions SET STY = (SELECT GROUP_CONCAT(MRSTY.TUI, '|') FROM MRSTY WHERE MRSTY.CUI = descriptions.CUI GROUP BY MRSTY.CUI)"
else
	echo "=> umls.db already exists"
fi

