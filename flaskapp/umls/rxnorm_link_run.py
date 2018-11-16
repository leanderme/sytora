#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	Run this script to perform the RxNorm linking process and store the
#	documents in a database or flat file.

import os
import sys
import logging

from rxnorm_link import runImport


class DocHandler(object):
	""" Superclass for simple database import.
	"""
	
	def __init__(self):
		self.documents = []
	
	def addDocument(self, doc):
		if doc is not None:
			self.documents.append(doc)
	
	def finalize(self):
		pass


class DebugDocHandler(DocHandler):
	""" Simply logs each new document.
	"""
	def addDocument(self, doc):
		print(doc)
	
	def __str__(self):
		return "Debug logger"


class SQLiteDocHandler(DocHandler):
	""" Handles documents for storage in sqlite3
	"""
	
	def __init__(self):
		super().__init__()
		from sqlite import SQLite
		absolute = os.path.dirname(os.path.realpath(__file__))
		db_file = os.environ.get('SQLITE_FILE')
		db_file = db_file if db_file else os.path.join(absolute, 'databases/rxnorm.db')
		self.db_file = db_file
		self.handled = 0

		self.sqlite = SQLite.get(self.db_file)
		self.sqlite.execute('DROP TABLE IF EXISTS drug_cache')

		self.sqlite.execute('''CREATE TABLE drug_cache
						(rxcui varchar, property text, value text)''')

		self.sqlite.execute('CREATE INDEX i_drug_cache ON drug_cache (rxcui, property)')

		self.sqlite.execute('DROP VIEW IF EXISTS drug_treatments_by_ndc')
		self.sqlite.execute('''CREATE VIEW drug_treatments_by_ndc as
				select a.value as ndc, b.value as treatment_intent
				from drug_cache a join drug_cache b on a.rxcui=b.rxcui
				where a.property='ndc' and b.property='treatment_intent'
				''')

		self.sqlite.execute('DROP VIEW IF EXISTS drug_classes_by_ndc')
		self.sqlite.execute('''CREATE VIEW drug_classes_by_ndc as
				select a.value as ndc, b.value as drug_class
				from drug_cache a join drug_cache b on a.rxcui=b.rxcui
				where a.property='ndc' and b.property='drug_class'
				''')

		self.sqlite.execute('DROP VIEW IF EXISTS drug_ingredients_by_ndc')
		self.sqlite.execute('''CREATE VIEW drug_ingredients_by_ndc as
				select a.value as ndc, b.value as drug_ingredient, c.str as ingredient_name
				from drug_cache a join drug_cache b on a.rxcui=b.rxcui
				join RXNCONSO c on c.rxcui=b.value
				where a.property='ndc' and b.property='ingredient'
				and c.sab='RXNORM' and c.tty='IN'
                ''')
	def addDocument(self, doc):
		rxcui =  doc.get('rxcui', '0')
		fields = {
			'tty': doc.get('tty', None),
			'ndc': doc.get('ndc', None),
			'label': doc.get('label', None),
			'drug_class': doc.get('drugClasses', None),
			'treatment_intent': doc.get('treatmentIntents', None),
			'ingredient': doc.get('ingredients', None)
			}
		for k, v in fields.items():
			if not v: continue
			v = v if isinstance(v, list) else [v]
			for vv in v:
				self.sqlite.execute(
					'INSERT INTO drug_cache(rxcui, property, value) values(?, ?, ?)',
					(rxcui, k, vv))
		self.handled += 1
		if (self.handled % 50 == 0): self.sqlite.commit()
		
	def finalize(self): 
		self.sqlite.commit()
	
	def __str__(self):
		return "SQLite import {}".format(self.db_file)


class MongoDocHandler(DocHandler):
	""" Handles documents for storage in MongoDB.
	"""
	
	def __init__(self):
		super().__init__()
		db_host = os.environ.get('MONGO_HOST')
		db_host = db_host if db_host else 'localhost'
		db_port = int(os.environ.get('MONGO_PORT'))
		db_port = db_port if db_port else 27017
		db_name = os.environ.get('MONGO_DB')
		db_name = db_name if db_name else 'default'
		db_bucket = os.environ.get('MONGO_BUCKET')
		db_bucket = db_bucket if db_bucket else 'rxnorm'
		
		import pymongo		# imported here so it's only imported when using Mongo
		conn = pymongo.MongoClient(host=db_host, port=db_port)
		db = conn[db_name]
		
		# authenticate
		db_user = os.environ.get('MONGO_USER')
		db_pass = os.environ.get('MONGO_PASS')
		if db_user and db_pass:
			db.authenticate(db_user, db_pass)
		
		self.mng = db[db_bucket]
		self.mng.ensure_index('ndc')
		self.mng.ensure_index('label', text=pymongo.TEXT)
	
	def addDocument(self, doc):
		lbl = doc.get('label')
		if lbl and len(lbl) > 1010:			# indexed, cannot be > 1024 in total
			doc['fullLabel'] = lbl
			doc['label'] = lbl[:1010]
		
		super().addDocument(doc)
		if len(self.documents) > 50:
			self._insertAndClear()
	
	def finalize(self):
		self._insertAndClear()
	
	def _insertAndClear(self):
		if len(self.documents) > 0:
			self.mng.insert(self.documents)
			self.documents.clear()
	
	def __str__(self):
		return "MongoDB at {}".format(self.mng)


class CSVHandler(DocHandler):
	""" Handles CSV export. """
	
	def __init__(self):
		super().__init__()
		self.csv_file = 'rxnorm.csv'
		self.csv_handle = open(self.csv_file, 'w')
		self.csv_handle.write("rxcui,tty,ndc,name,va_classes,treating,ingredients\n")
	
	def addDocument(self, doc):
		self.csv_handle.write('{},"{}","{}","{}","{}","{}","{}"{}'.format(
			doc.get('rxcui', '0'),
			doc.get('tty', ''),
			doc.get('ndc', ''),
			doc.get('label', ''),
			';'.join(doc.get('drugClasses') or []),
			';'.join(doc.get('treatmentIntents') or []),
			';'.join(doc.get('ingredients') or []),
			"\n"
		))
	
	def __str__(self):
		return 'CSV file "{}"'.format(self.csv_file)


def runLinking(ex_type):
	""" Create the desired handler and run import.
	"""
	handler = DebugDocHandler()
	if ex_type is not None and len(ex_type) > 0:
		try:
			if 'mongo' == ex_type:
				handler = MongoDocHandler()
			elif 'couch' == ex_type:
				# import couchbase
				raise Exception('Couchbase not implemented')
			elif 'csv' == ex_type:
				handler = CSVHandler()
			elif 'sqlite' == ex_type:
				handler = SQLiteDocHandler()
			else:
				raise Exception('Unsupported export type: {}'.format(ex_type))
		except Exception as e:
			logging.error(e)
			sys.exit(1)
	
	print('->  Processing to {}'.format(handler))
	runImport(doc_handler=handler)


if '__main__' == __name__:
	logging.basicConfig(level=logging.INFO)
	
	cmd_arg = sys.argv[1] if len(sys.argv) > 1 else None
	ex_type = os.environ.get('EXPORT_TYPE') or cmd_arg
	
	runLinking(ex_type)

