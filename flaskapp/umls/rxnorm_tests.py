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
from rxnorm import RxNorm


class RxNormTest(unittest.TestCase):
	""" Test :class:`RxNorm`.
	"""
	
	def test_ndc_normalization(self):
		""" Test NDC normalization.
		"""
		# 6-4-2
		self.assertEqual('00074148614', RxNorm.ndc_normalize('000074-1486-14'))
		self.assertEqual('51227615900', RxNorm.ndc_normalize('051227-6159-**'))
		self.assertEqual('58734000101', RxNorm.ndc_normalize('058734-0001-*1'))
		
		# 6-4-1
		self.assertEqual('00854684102', RxNorm.ndc_normalize('000854-6841-2'))
		
		# 6-4: treat as 6-4-2 with two trailing zeroes
		self.assertEqual('57982011000', RxNorm.ndc_normalize('057982-0110'))
		self.assertEqual('12579005600', RxNorm.ndc_normalize('012579-*056'))
		
		# 6-3-2
		self.assertEqual('57982012312', RxNorm.ndc_normalize('057982-123-12'))
		
		# 6-3-1
		self.assertEqual('57982098709', RxNorm.ndc_normalize('057982-987-9'))
		
		# 5-4-2
		self.assertEqual('17317093201', RxNorm.ndc_normalize('17317-0932-01'))
		
		# 5-4-1
		self.assertEqual('36987315601', RxNorm.ndc_normalize('36987-3156-1'))
		
		# 5-3-2
		self.assertEqual('24730041205', RxNorm.ndc_normalize('24730-412-05'))
		
		# 4-4-2
		self.assertEqual('00268010310', RxNorm.ndc_normalize('0268-0103-10'))
		
		# 12 digit VANDF
		self.assertEqual('03475476541', RxNorm.ndc_normalize('003475476541'))
		
		# normalized already
		self.assertEqual('04458632698', RxNorm.ndc_normalize('04458632698'))
		
		# invalid
		self.assertIsNone(RxNorm.ndc_normalize('0054478962'))
		self.assertIsNone(RxNorm.ndc_normalize('547668531244'))
		self.assertIsNone(RxNorm.ndc_normalize('0054478962796'))
		self.assertIsNone(RxNorm.ndc_normalize('0a79b2-c87-9'))
		self.assertIsNone(RxNorm.ndc_normalize('si-lly-te-st'))
		self.assertIsNone(RxNorm.ndc_normalize('just-a-rand-test-string'))
