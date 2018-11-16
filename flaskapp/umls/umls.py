#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	Utilities to handle UMLS
#
#	2013-01-01	Created by Pascal Pfiffner
#	2014-01-20	Extracted and converted to Python 3
#


import sys
import os.path
import logging

from sqlite import SQLite			# for py-umls standalone

reload(sys)
sys.setdefaultencoding('utf-8')

class UMLS (object):
	""" A class for importing UMLS terminologies into an SQLite database.
	"""
	
	@classmethod
	def check_database(cls):
		""" Check if our database is in place and if not, prompts to import it.
		Will raise on errors!
		
		UMLS: (umls.db)
		If missing prompt to use the `umls.sh` script
		"""
		
		umls_db = os.path.join('databases', 'umls.db')
		if not os.path.exists(umls_db):
			raise Exception("The UMLS database at {} does not exist. Run the import script `databases/umls.sh`."
				.format(os.path.abspath(umls_db)))



class UMLSLookup (object):
	""" UMLS lookup """
	
	sqlite = None
	did_check_dbs = False
	preferred_sources = ['"SNOMEDCT"', '"MTH"', '"ICPCGER"']	
	
	def __init__(self):
		absolute = os.path.dirname(os.path.realpath(__file__))
		self.sqlite = SQLite.get(os.path.join(absolute, 'databases/umls.db'))
	
	def lookup_code(self, cui, preferred=True, lat='ENG'):
		""" Return a list with triples that contain:
		- name
		- source
		- semantic type
		by looking it up in our "descriptions" database.
		The "preferred" settings has the effect that only names from SNOMED
		(SNOMEDCD) and the Metathesaurus (MTH) will be reported. A lookup in
		our "descriptions" table is much faster than combing through the full
		MRCONSO table.
		
		:returns: A list of triples with (name, sab, sty)
		"""
		if cui is None or len(cui) < 1:
			return []
		
		# lazy UMLS db checking
		if not UMLSLookup.did_check_dbs:
			UMLS.check_database()
			UMLSLookup.did_check_dbs = True
		
		# take care of negations
		negated = '-' == cui[0]
		if negated:
			cui = cui[1:]
		
		parts = cui.split('@', 1)
		lookup_cui = parts[0]
		
		# STR: Name
		# SAB: Abbreviated Source Name
		# STY: Semantic Type
		if preferred:
			sql = 'SELECT DISTINCT STR, SAB, STY FROM descriptions WHERE LAT = "{lng}" AND CUI = ? AND SAB IN ({pref}) LIMIT 1'.format(pref=", ".join(UMLSLookup.preferred_sources), lng=lat)
		else:
			sql = 'SELECT DISTINCT STR, SAB, STY FROM descriptions WHERE LAT = "{lng}" AND CUI = ? LIMIT 1'.format(lng=lat)
		# return as list
		arr = []
		for res in self.sqlite.execute(sql, (lookup_cui,)):
			arr.append(res)
		
		return arr
	
	
	def lookup_code_meaning(self, cui, preferred=True, no_html=True, lat='ENG', destinct=False):
		""" Return a string (an empty string if the cui is null or not found)
		by looking it up in our "descriptions" database.
		The "preferred" settings has the effect that only names from SNOMED
		(SNOMEDCD) and the Metathesaurus (MTH) will be reported. A lookup in
		our "descriptions" table is much faster than combing through the full
		MRCONSO table.
		"""
		names = []
		for res in self.lookup_code(cui, preferred, lat):
			names.append(str(res[0].decode('utf8')))
		return names if len(names) > 0 else []
	
	
	def lookup_code_for_name(self, name, preferred=True):
		""" Tries to find a good concept code for the given concept name.
		
		Uses our indexed `descriptions` table.
		
		:returns: A list of triples with (cui, sab, sty)
		"""

		if name is None or len(name) < 1:
			return None
		
		# lazy UMLS db checking
		if not UMLSLookup.did_check_dbs:
			UMLS.check_database()
			UMLSLookup.did_check_dbs = True
		
		# CUI: Concept-ID
		# STR: Name
		# SAB: Abbreviated Source Name
		# STY: Semantic Type
		if preferred:
			sql = 'SELECT DISTINCT CUI, SAB, STY FROM descriptions WHERE STR LIKE ? AND SAB IN ({})'.format(", ".join(UMLSLookup.preferred_sources))
		else:
			sql = 'SELECT DISTINCT CUI, SAB, STY FROM descriptions WHERE STR LIKE ?'
		
		# return as list
		arr = []
		for res in self.sqlite.execute(sql, ('%' + name + '%',)):
			arr.append(res)
		
		return arr



# running this as a script does the database setup/check
if '__main__' == __name__:
	UMLS.check_database()
	
	# examples
	look = UMLSLookup()
	code = 'C0877430'
	meaning = look.lookup_code_meaning(code, lat='GER', preferred=False)
	print('UMLS code "{0}":  {1}'.format(code, meaning))
	