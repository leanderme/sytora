#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  LOINC import and lookup utilities


import sys
import os.path
import logging


class LOINCLookup(object):
	pass


class LOINC(object):
	""" Class that helps with setting up a local LOINC SQLite database.
	"""
	
	@classmethod
	def check_database(cls):
		""" Check if our database is in place and if not, prompts to create it.
		Will raise on errors!
		
		Reads LOINC from CSV files and create an SQLite database, if needed.
		"""
		
		dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'databases/loinc.db')
		if not os.path.exists(dbpath):
			raise Exception("The LOINC database at {} does not exist. Run the script `loinc.py`."
				.format(dbpath))
	
	@classmethod
	def import_from_files(cls, dirpath):
		""" Imports LOINC from the downloaded CSV files.
		"""
		import sqlite
		import csvimporter
		
		mapping = {
			'loinc.csv': 'loinc',
			'map_to.csv': 'map_to',
			'source_organization.csv': 'sources'
		}
		dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'databases/loinc.db')
		
		# import
		for csvfile, table in mapping.items():
			print("Importing LOINC table {}".format(csvfile))
			imp = csvimporter.CSVImporter(os.path.join(dirpath, csvfile), table)
			imp.import_to(dbpath)
		
		# index
		print("Creating indexes")
		sql_handle = sqlite.SQLite(dbpath)
		sql_handle.execute('CREATE INDEX x_loinc_num_loinc ON loinc (LOINC_NUM)')
		sql_handle.execute('CREATE INDEX x_shortname_loinc ON loinc (SHORTNAME)')
		sql_handle.execute('CREATE INDEX x_long_common_name_loinc ON loinc (LONG_COMMON_NAME)')



# running this as a script performs the database setup/check
if '__main__' == __name__:
	logging.basicConfig(level=logging.DEBUG)
	
	# if the database check fails, run import commands
	try:
		LOINC.check_database()
	except Exception as e:
		csv_path = sys.argv[1] if 2 == len(sys.argv) else None
		if csv_path is not None and os.path.exists(csv_path):
			try:
				LOINC.import_from_files(csv_path)
			except Exception as e:
				raise Exception("SNOMED import failed: {}".format(e))
		else:
			print("Provide the path to the directory containing the LOINC CSV files as first argument.")
			print("Download the LOINC Table File in CSV format (free registration required) here:")
			print("http://loinc.org/downloads/loinc")
	
	# TODO: lookup examples
