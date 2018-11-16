#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	RxNorm unit testing
#
#	2014-04-18	Created

import sys
import os.path
thismodule = os.path.abspath(os.path.dirname(__file__))
if thismodule not in sys.path:
	sys.path.insert(0, thismodule)

import unittest
from snomed import *


class SNOMEDLookupTest(unittest.TestCase):
	""" Test :class:`SNOMEDLookup`.
	"""
	def setUp(self):
		SNOMED.check_database()
	
	def test_term_lookup(self):
		""" Test term lookup.
		"""
		cpt = SNOMEDConcept('215350009')
		self.assertEqual(cpt.term, 'Accident involving being caught in door of road vehicle NEC, occupant of tram injured (event)')
		cpt = SNOMEDConcept('315004001')
		self.assertEqual(cpt.term, 'Metastasis from malignant tumor of breast')
	
	def test_hierarchy_isa(self):
		""" Test hierarchical lookup.
		"""
		cpt = SNOMEDConcept('315004001')        # Metastasis from malignant tumor of breast
		child = SNOMEDConcept('128462008')      # Metastatic neoplasm (disease)
		self.assertTrue(cpt.isa(child.code))
		child = SNOMEDConcept('363346000')      # Malignant neoplastic disease (disorder)
		self.assertTrue(cpt.isa(child))
		child = SNOMEDConcept('55342001')       # Neoplasia
		self.assertTrue(cpt.isa(child.code))
		child = SNOMEDConcept('408643008')      # Infiltrating duct carcinoma of breast
		self.assertFalse(cpt.isa(child.code))
	
