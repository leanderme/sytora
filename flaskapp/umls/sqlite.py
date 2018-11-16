#!/usr/bin/env python3
#
#	Simplifying SQLite access
#
#	2012-12-14	Created by Pascal Pfiffner
#


import sqlite3
import threading


SQLITE_INSTANCES = {}


class SQLite(object):
	""" SQLite access
	"""

	@classmethod
	def get(cls, database):
		""" Use this to get SQLite instances for a given database. Avoids
		creating multiple instances for the same database.
		
		We keep instances around per thread per database, maybe there should be
		a way to turn this off. However, here we always release instances for
		threads that are no longer alive. If this is better than just always
		creating a new instance should be tested.
		"""
		
		global SQLITE_INSTANCES
		
		# group per thread
		thread_id = threading.current_thread().ident
		if thread_id not in SQLITE_INSTANCES:
			SQLITE_INSTANCES[thread_id] = {}
		by_thread = SQLITE_INSTANCES[thread_id]
		
		# group per database
		if database not in by_thread:
			sql = SQLite(database)
			by_thread[database] = sql
		
		# free up memory for terminated threads
		clean = {}
		for alive in threading.enumerate():
			if alive.ident in SQLITE_INSTANCES:
				clean[alive.ident] = SQLITE_INSTANCES[alive.ident]
		SQLITE_INSTANCES = clean
		
		return by_thread[database]


	def __init__(self, database=None):
		if database is None:
			raise Exception('No database provided')
		
		self.database = database
		self.handle = None
		self.cursor = None


	def execute(self, sql, params=()):
		""" Executes an SQL command and returns the cursor.execute, which can
		be used as an iterator.
		Supply the params as tuple, i.e. (param,) and (param1, param2, ...)
		"""
		if not sql or 0 == len(sql):
			raise Exception('No SQL to execute')
		if not self.cursor:
			self.connect()
		
		return self.cursor.execute(sql, params)


	def executeInsert(self, sql, params=()):
		""" Executes an SQL command (should be INSERT OR REPLACE) and returns
		the last row id, 0 on failure.
		"""
		if self.execute(sql, params):
			return self.cursor.lastrowid if self.cursor.lastrowid else 0
		
		return 0


	def executeUpdate(self, sql, params=()):
		""" Executes an SQL command (should be UPDATE) and returns the number
		of affected rows.
		"""
		if self.execute(sql, params):
			return self.cursor.rowcount
		
		return 0


	def executeOne(self, sql, params):
		""" Returns the first row returned by executing the command
		"""
		self.execute(sql, params)
		return self.cursor.fetchone()


	def hasTable(self, table_name):
		""" Returns whether the given table exists. """
		sql = 'SELECT COUNT(*) FROM sqlite_master WHERE type="table" and name=?'
		ret = self.executeOne(sql, (table_name,))
		return True if ret and ret[0] > 0 else False
	
	def create(self, table_name, table_structure):
		""" Executes a CREATE TABLE IF NOT EXISTS query with the given structure.
		Input is NOT sanitized, watch it!
		"""
		create_query = 'CREATE TABLE IF NOT EXISTS %s %s' % (table_name, table_structure)
		self.execute(create_query)
		return True


	def commit(self):
		self.handle.commit()

	def rollback(self):
		self.handle.rollback()


	def connect(self):
		if self.cursor is not None:
			return
		
		self.handle = sqlite3.connect(self.database)
		self.cursor = self.handle.cursor()

	def close(self):
		if self.cursor is None:
			return

		self.handle.close()
		self.cursor = None
		self.handle = None

