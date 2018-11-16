#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Simple CSV importer.

import re
import csv
import sqlite3


class CSVImporter(object):
	""" A simple CSV to SQLite importer class.
	
	Expects a CSV file with a header row, will create a table reflecting the
	header row and import all rows.
	"""
	_sqlite = None
	
	def __init__(self, csv_path, tablename='rows'):
		self.filepath = csv_path
		self.tablename = tablename
	
	def sqlite_handle(self, dbpath):
		if self._sqlite is None:
			self._sqlite = sqlite3.connect(dbpath)
		return self._sqlite
	
	def import_to(self, dbpath, csv_format='excel'):
		assert self.filepath
		assert dbpath
		
		# SQLite handling
		sql_handle = self.sqlite_handle(dbpath)
		sql_handle.isolation_level = 'EXCLUSIVE'
		sql_cursor = sql_handle.cursor()
		create_sql = 'CREATE TABLE {} '.format(self.tablename)
		insert_sql = 'INSERT INTO {} '.format(self.tablename)
		all_but_alnum = r'\W+'
		
		# loop rows
		with open(self.filepath, 'r') as csv_handle:
			reader = csv.reader(csv_handle, quotechar='"', dialect=csv_format)
			try:
				i = 0
				for row in reader:
					sql = insert_sql
					params = ()
					
					# first row is the header row
					if 0 == i:
						fields = []
						fields_create = []
						for field in row:
							field = re.sub(all_but_alnum, '', field)
							fields.append(field)
							fields_create.append('{} VARCHAR'.format(field))
						
						create_sql += "(\n\t{}\n)".format(",\n\t".join(fields_create))
						sql = create_sql
						
						insert_sql += '({}) VALUES ({})'.format(', '.join(fields), ', '.join(['?' for i in range(len(fields))]))
					
					# data rows
					else:
						params = tuple(row)
					
					# execute SQL statement
					try:
						sql_cursor.execute(sql, params)
					except Exception as e:
						sys.exit(u'SQL failed: %s  --  %s' % (e, sql))
					i += 1
				
				# commit to file
				sql_handle.commit()
				sql_handle.isolation_level = None
			
			except csv.Error as e:
				sys.exit('CSV error on line %d: %s' % (reader.line_num, e))

