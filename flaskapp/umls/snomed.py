#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	SNOMED import utilities, extracted from umls.py
#
#	2014-01-20	Created by Pascal Pfiffner
#

import sys
import os
import csv
import logging

from sqlite import SQLite			# for py-umls standalone


class SNOMEDDBNotPresentException(Exception):
	pass

class SNOMED(object):
	""" A class for importing UMLS terminologies into an SQLite database.
	"""
	sqlite_handle = None
	
	@classmethod
	def database_path(cls):
		absolute = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(absolute, 'databases/snomed.db')
	
	@classmethod
	def check_database(cls):
		""" Check if our database is in place and if not, prompts to create it.
		Will raise on errors!
		
		SNOMED: (snomed.db)
		Read SNOMED CT from tab-separated files and create an SQLite database.
		"""
		snomed_db = cls.database_path()
		if not os.path.exists(snomed_db):
			raise SNOMEDDBNotPresentException("The SNOMED database at {} does not exist. Run the script `snomed.py`."
				.format(os.path.abspath(snomed_db)))
	
	@classmethod
	def find_needed_files(cls, snomed_dir):
		
		# table to file mapping
		prefixes = {
			'descriptions': 'sct2_Description_Full-en_',
			'relationships': 'sct2_Relationship_Full_'
		}
		found = {}
		snomed_dir = sys.argv[1]
		
		# try to find the files
		for table, prefix in prefixes.items():
			found_file = _find_files(snomed_dir, prefix)
			if found_file is None:
				raise Exception('Unable to locate file starting with "{}" in SNOMED directory at {}'.format(prefix, snomed_dir))
			found[table] = found_file
		
		return found
	
	@classmethod
	def import_from_files(cls, rx_map):
		for table, filepath in rx_map.items():
			num_query = 'SELECT COUNT(*) FROM {}'.format(table)
			num_existing = cls.sqlite_handle.executeOne(num_query, ())[0]
			if num_existing > 0:
				continue
			
			cls.import_csv_into_table(filepath, table)
	
	@classmethod
	def import_csv_into_table(cls, snomed_file, table_name):
		""" Import SNOMED CSV into our SQLite database.
		The SNOMED CSV files can be parsed by Python's CSV parser with the
		"excel-tab" flavor.
		"""
		
		logging.debug('Importing SNOMED {} into snomed.db...'.format(table_name))
		
		# not yet imported, parse tab-separated file and import
		with open(snomed_file, encoding='utf-8') as csv_handle:
			cls.sqlite_handle.isolation_level = 'EXCLUSIVE'
			sql = cls.insert_query_for(table_name)
			reader = csv.reader(csv_handle, dialect='excel-tab')
			i = 0
			try:
				for row in reader:
					if i > 0:			# first row is the header row
						
						# execute SQL (we just ignore duplicates)
						params = cls.insert_tuple_from_csv_row_for(table_name, row)
						try:
							cls.sqlite_handle.execute(sql, params)
						except Exception as e:
							sys.exit('Cannot insert {}: {}'.format(params, e))
					i += 1
				
				# commit to file
				cls.sqlite_handle.commit()
				cls.did_import(table_name)
				cls.sqlite_handle.isolation_level = None
			
			except csv.Error as e:
				cls.sqlite_handle.rollback()
				sys.exit('CSV error on line {}: {}'.format(reader.line_num, e))

		logging.debug('{} concepts parsed'.format(i-1))


	@classmethod
	def setup_tables(cls):
		""" Creates the SQLite tables we need, not the tables we deserve.
		Does nothing if the tables/indexes already exist
		"""
		if cls.sqlite_handle is None:
			cls.sqlite_handle = SQLite.get(cls.database_path())
		
		# descriptions
		cls.sqlite_handle.create('descriptions', '''(
				concept_id INTEGER PRIMARY KEY,
				lang TEXT,
				term TEXT,
				isa VARCHAR,
				active INT
			)''')
		
		# relationships
		cls.sqlite_handle.create('relationships', '''(
				relationship_id INTEGER PRIMARY KEY,
				source_id INT,
				destination_id INT,
				rel_type INT,
				rel_text VARCHAR,
				active INT
			)''')
	
	@classmethod
	def insert_query_for(cls, table_name):
		""" Returns the insert query needed for the given table
		"""
		if 'descriptions' == table_name:
			return '''INSERT OR IGNORE INTO descriptions
						(concept_id, lang, term, isa, active)
						VALUES
						(?, ?, ?, ?, ?)'''
		if 'relationships' == table_name:
			return '''INSERT OR IGNORE INTO relationships
						(relationship_id, source_id, destination_id, rel_type, active)
						VALUES
						(?, ?, ?, ?, ?)'''
		return None
	
	@classmethod
	def insert_tuple_from_csv_row_for(cls, table_name, row):
		if 'descriptions' == table_name:
			isa = ''
			if len(row) > 6:
				if '900000000000013009' == row[6]:
					isa = 'synonym'
				elif '900000000000003001' == row[6]:
					isa = 'full'
			return (int(row[4]), row[5], row[7], isa, int(row[2]))
		if 'relationships' == table_name:
			return (int(row[0]), int(row[4]), int(row[5]), int(row[7]), int(row[2]))
		return None
	
	@classmethod
	def did_import(cls, table_name):
		""" Allows us to set hooks after tables have been imported.
		
		Creates indexes and names `isa` and `finding_site` relationships.
		"""
		# index descriptions
		if 'descriptions' == table_name:
			print("----- DID IMPORT descriptions")
			cls.sqlite_handle.execute("CREATE INDEX IF NOT EXISTS isa_index ON descriptions (isa)")
		
		# update and index relationships
		if 'relationships' == table_name:
			print("----- DID IMPORT relationships")
			cls.sqlite_handle.execute("UPDATE relationships SET rel_text = 'isa' WHERE rel_type = 116680003")
			cls.sqlite_handle.execute("UPDATE relationships SET rel_text = 'finding_site' WHERE rel_type = 363698007")
			cls.sqlite_handle.execute("CREATE INDEX IF NOT EXISTS source_index ON relationships (source_id)")
			cls.sqlite_handle.execute("CREATE INDEX IF NOT EXISTS destination_index ON relationships (destination_id)")
			cls.sqlite_handle.execute("CREATE INDEX IF NOT EXISTS rel_text_index ON relationships (rel_text)")


class SNOMEDLookup(object):
	""" SNOMED lookup """
	
	sqlite = None
	
	def __init__(self):
		self.sqlite = SQLite.get(SNOMED.database_path())
	
	def lookup_code_meaning(self, snomed_id, preferred=True, no_html=True):
		""" Returns HTML for all matches of the given SNOMED id.
		The "preferred" flag here currently has no function.
		"""
		if snomed_id is None or len(snomed_id) < 1:
			return ''
		
		sql = 'SELECT term, isa, active FROM descriptions WHERE concept_id = ?'
		names = []
		
		# loop over results
		for res in self.sqlite.execute(sql, (snomed_id,)):
			if not no_html and ('synonym' == res[1] or 0 == res[2]):
				names.append("<span style=\"color:#888;\">{}</span>".format(res[0]))
			else:
				names.append(res[0])
		
		if no_html:
			return ", ".join(names) if len(names) > 0 else ''
		return "<br/>\n".join(names) if len(names) > 0 else ''
	
	def lookup_if_isa(self, child_id, parent_id, checked=None):
		""" Determines if a child concept is refining a parent concept, i.e.
		if there is a (direct or indirect) "is a" (116680003) relationship from
		child to parent.
		"""
		if not child_id or not parent_id:
			return False
		if checked is not None and child_id in checked:
			return False
		
		parents = self.lookup_parents_of(child_id)
		if parent_id in parents:
			return True
		
		chkd = checked or []
		chkd.append(child_id)
		for parent in parents:
			flag = self.lookup_if_isa(parent, parent_id, chkd)
			if flag:
				return True
		return False
	
	def lookup_parents_of(self, snomed_id):
		""" Returns a list of concept ids that have a direct "is a" (116680003)
		relationship with the given id.
		"""
		ids = []
		if snomed_id:
			#sql = 'SELECT destination_id FROM relationships WHERE source_id = ? AND rel_type = 116680003'	# Too slow!!
			sql = 'SELECT destination_id, rel_text FROM relationships WHERE source_id = ?'
			for res in self.sqlite.execute(sql, (snomed_id,)):
				if 'isa' == res[1]:
					ids.append(str(res[0]))
		return ids


class SNOMEDConcept(object):
	""" Represents a SNOMED concept.
	"""
	uplooker = SNOMEDLookup()
	
	def __init__(self, code):
		self.code = code
		self._term = None
	
	@property
	def term(self):
		if self._term is None:
			self._term = self.__class__.uplooker.lookup_code_meaning(self.code)
		return self._term
	
	def isa(self, parent_code):
		""" Checks whether the receiver is a child of the given code.
		The `parent_code` argument can also be a :class:`SNOMEDConcept`
		instance.
		
		:returns: A bool on whether the receiver is a child of the given
		    concept
		"""
		if isinstance(parent_code, SNOMEDConcept):
			return self.__class__.uplooker.lookup_if_isa(self.code, parent_code.code)
		return self.__class__.uplooker.lookup_if_isa(self.code, parent_code)


# find file function
def _find_files(directory, prefix):
	for root, dirs, files in os.walk(directory):
		for name in files:
			if name.startswith(prefix):
				return os.path.join(directory, name)
		
		for name in dirs:
			found = _find_files(os.path.join(directory, name), prefix)
			if found:
				return found
	return None


# running this as a script does the database setup/check
if '__main__' == __name__:
	logging.basicConfig(level=logging.DEBUG)
	
	# if the database check fails, run import commands
	try:
		SNOMED.check_database()
	except SNOMEDDBNotPresentException as e:
		if len(sys.argv) < 2:
			print("Provide the path to the extracted SNOMED (RF2) directory as first argument.")
			print("Download SNOMED from http://www.nlm.nih.gov/research/umls/licensedcontent/snomedctfiles.html""")
			sys.exit(0)
		
		# import from files
		try:
			found = SNOMED.find_needed_files(sys.argv[1])
			SNOMED.sqlite_handle = None
			SNOMED.setup_tables()
			SNOMED.import_from_files(found)
		except Exception as e:
			print("SNOMED import failed: {}".format(e))
		sys.exit(0)
	
	# examples
	cpt = SNOMEDConcept('215350009')
	print('SNOMED code "{0}":  {1}'.format(cpt.code, cpt.term))
	
	cpt = SNOMEDConcept('315004001')	# -> 128462008 -> 363346000 -> 55342001 x> 215350009
	for other, expected in [('128462008', True), ('363346000', True), ('55342001', True), ('215350009', False)]:
		print('SNOMED code "{0}" refines "{1}":  {2}'.format(cpt.code, other, cpt.isa(other)))
		assert expected == cpt.isa(other), '"{0}" refines "{1}" should return {2} or the database hasn’t been set up properly'.format(cpt.code, other, 'True' if expected else 'False')

