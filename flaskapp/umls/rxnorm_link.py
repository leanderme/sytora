#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	Precompute interesting RXCUI relationships into a dictionary. Use the script
#	`rxnorm_link_run.sh` to store these dictionaries into a JSON database. See
#	that script for parameters to change.
#
#	2012-09-28	Created by Josh Mandel
#	2014-02-10	Stolen by Pascal Pfiffner
#
#	For profiling: pycallgraph graphviz -- rxnorm_link.py

import sys
import os.path
sys.path.insert(0, os.path.dirname(__file__))

import json
import signal
import logging
from datetime import datetime

from rxnorm import RxNorm, RxNormLookup


def doQ(rxhandle, q, p):
	return [x[0] for x in rxhandle.fetchAll(q, p)]

def toBrandAndGeneric(rxhandle, rxcuis, tty):
	ret = set()
	for rxcui in rxcuis:
		ret.update(doQ(rxhandle, "SELECT rxcui1 from rxnrel where rxcui2=? and rela='tradename_of'", (rxcui,)))
	return ret

def toComponents(rxhandle, rxcuis, tty):
	ret = set()

	if tty not in ("SBD", "SCD"):
		return ret

	for rxcui in rxcuis:
		cs = doQ(rxhandle, "SELECT rxcui1 from rxnrel where rxcui2=? and rela='consists_of'", (rxcui,))
		for c in cs:
			ret.update(doQ(rxhandle, "SELECT rxcui from rxnconso where rxcui=? and sab='RXNORM' and tty='SCDC'", (c,)))        

	return ret

def toTreatmentIntents(rxhandle, rxcuis, tty):
	ret = set()
	for rxcui in rxcuis:
		ret.update(toTreatmentIntents_helper(rxhandle, rxcui, tty))
	return ret

def toTreatmentIntents_helper(rxhandle, rxcui, tty):
	assert tty=='IN'
	ret = []
	rxauis = doQ(rxhandle, "SELECT rxaui from rxnconso where rxcui=? and tty='FN' and sab='NDFRT'", (rxcui,))
	for rxaui in rxauis:
		rxauis1 = doQ(rxhandle, "SELECT rxaui1 from rxnrel where rxaui2=? and rela='may_treat'", (rxaui,))
		for rxaui1 in rxauis1:
			name = doQ(rxhandle, "SELECT str from rxnconso where rxaui=? and tty='FN' and sab='NDFRT'", (rxaui1,))
			name = map(lambda x: x.replace(" [Disease/Finding]", ""), name)
			ret.extend(name)
	return ret

def toMechanism(rxhandle, rxcuis, tty):
	ret = set()
	for v in rxcuis:
		ret.update(toMechanism_helper(rxhandle, v, tty))
	return ret

def toMechanism_helper(rxhandle, rxcui, tty):
	assert tty=='IN'
	ret = set()
	rxauis = doQ(rxhandle, "SELECT rxaui from rxnconso where rxcui=? and tty='FN' and sab='NDFRT'", (rxcui,))
	for a in rxauis:
		a1 = doQ(rxhandle, "SELECT rxaui1 from rxnrel where rxaui2=? and rela='has_mechanism_of_action'", (a,))
		if len(a1) > 0:
			moa = doQ(rxhandle, "SELECT str from rxnconso where rxaui=? and tty='FN' and sab='NDFRT'", (a1[0],))
			moa = map(lambda x: x.replace(" [MoA]", ""), moa)
			ret.update(moa)
	return ret


def toIngredients(rxhandle, rxcuis, tty):
	ret = set()
	for v in rxcuis:
		ret.update(toIngredients_helper(rxhandle, v, tty))
	return ret

def toIngredients_helper(rxhandle, rxcui, tty):
	if 'IN' == tty:
		return []
	
	# can lookup ingredient directly
	map_direct = {
		'MIN': 'has_part',
		'PIN': 'form_of',
		'BN': 'tradename_of',
		'SCDC': 'has_ingredient',
		'SCDF': 'has_ingredient',
		'SCDG': 'has_ingredient',
	}
	
	if tty in map_direct:
		return doQ(rxhandle, "SELECT rxcui1 from rxnrel where rxcui2=? and rela=?", (rxcui, map_direct[tty]))
	
	# indirect ingredient lookup
	map_indirect = {
		'BPCK': ('contains', 'SCD'),
		'GPCK': ('contains', 'SCD'),
		'SBD': ('tradename_of', 'SCD'),
		'SBDC': ('tradename_of', 'SCDC'),
		'SBDF': ('tradename_of', 'SCDF'),
		'SBDG': ('tradename_of', 'SCDG'),
		'SCD': ('consists_of', 'SCDC'),
	}
	
	if tty in map_indirect:
		val = map_indirect[tty]
		return toIngredients(rxhandle, doQ(rxhandle, "SELECT rxcui1 from rxnrel where rxcui2=? and rela=?", (rxcui, val[0])), val[1])
	
	logging.warn('TTY "{}" is not mapped, skipping ingredient lookup'.format(tty))
	return []


def initVA(rxhandle):
	""" Initializes the VA drug class cache table and inserts all known drug
	classes by looking them up in the RXNSAT table (ATN = "VA_CLASS_NAME").
	"""
	# SELECT DISTINCT tty, COUNT(tty) FROM rxnsat LEFT JOIN rxnconso AS r USING (rxcui) WHERE atn = "VA_CLASS_NAME" GROUP BY tty;
	rxhandle.execute('DROP TABLE IF EXISTS va_cache')
	rxhandle.execute('''CREATE TABLE va_cache
						(rxcui varchar UNIQUE, va text, from_rxcui varchar, rela varchar, level int)''')
	rxhandle.execute('''INSERT OR IGNORE INTO va_cache
						SELECT rxcui, atv, null, null, 0 FROM rxnsat
						WHERE atn = "VA_CLASS_NAME"''')
	rxhandle.sqlite.commit()

def traverseVA(rxhandle, rounds=3, expect=203175):
	""" Drug classes are set for a couple of different TTYs, it seems however
	most consistently to be defined on CD, SCD and AB TTYs.
	We cache the classes in va_cache and loop over rxcuis with known classes,
	applying the known classes to certain relationships.
	"""
	print("->  Starting VA class mapping")
	
	mapping = {
		'CD': [
			'has_tradename',			# > BD, SBD, ... ; tiny impact on step 2, compensated for in steps 3+
			'contained_in',				# > BPCK; tiny impact in step 2, compansated for in steps 3+
			'consists_of',				# > SCDC; big impact step 2+, starting to be compensated for in steps 5+; NOT IDEAL
			#'quantified_form',			# > SBD; no impact
		],
		'GPCK': [
			'has_tradename',			# > BPCK; small impact step 3
		],
		
		'SBD': [
			'isa',						# > SBDF; big impact step 2+, increasingly important (58% vs 75% coverage after step 5)
			'has_ingredient',			# > BN; small impact step 2+
			'tradename_of',				# > SCD; tiny impact step 2, fully compensated by step 4
			'consists_of',				# > SBDC; small impact step 4+
		],
		'SBDF': [
			#'tradename_of',			# > SCDF; no impact
			'has_ingredient',			# > BN; tiny impact step 2+
			#'inverse_isa',				# > SBD; no impact
		],
		'SBDG': [
			'has_ingredient',			# > BN; tiny impact step 2+
			#'tradename_of',			# > SCDG; no impact
		],
		'SBDC': [
			'tradename_of',				# > SCDC; tiny impact step 3, compensated by step 5
		],
		
		'SCD': [
			'isa',						# > SCDF; big impact step 2+, not compensated (59% vs 75% coverage after step 5)
			'has_quantified_form',		# > SCD; tiny impact step 2, fully compensated in step 3
			'contained_in',				# > GPCK; tiny impact steps 4+
			'has_tradename',			# > SBD; small impact steps 3+
		],
		'SCDC': [
			'constitutes',				# > SCD; big impact steps 3+ (63% vs 75% coverage after step 5)
			'has_tradename',			# > SBDC; impact in step 3, partially compensated in step 4
		],
		'SCDF': [
			'inverse_isa',				# > SCD; large impact steps 3+
		],
		'SCDG': [
			#'tradename_of',			# > SBDG; no impact
		]
	}
	
	found = set()
	per_level_sql = 'SELECT rxcui, va FROM va_cache WHERE level = ?'
	
	for l in range(0,rounds):
		i = 0
		existing = rxhandle.fetchAll(per_level_sql, (l,))
		num_drugs = len(existing)
		this_round = set();
		
		# loop all rxcuis that already have a class and walk their relationships
		for rxcui, va_imp in existing:
			found.add(rxcui)
			this_round.add(rxcui)
			vas = va_imp.split('|')
			seekRelAndStoreSameVAs(rxhandle, rxcui, set(vas), mapping, l)
			
			# progress report
			i += 1
			print('-->  Step {}  {:.1%}'.format(l+1, i / num_drugs), end="\r")
		
		# commit after every round
		rxhandle.sqlite.commit()
		print('==>  Step {}, found classes for {} of {} drugs, {:.2%} coverage'.format(l+1, len(this_round), expect, len(found) / expect))
	
	print('->  VA class mapping complete')

def seekRelAndStoreSameVAs(rxhandle, rxcui, vas, mapping, at_level=0):
	""" For the given RXCUI retrieves all relations, as defined in `mapping`,
	and updates those concepts with the drug classes passed in in `vas`.
	"""
	assert(rxcui)
	assert(len(vas) > 0)
	
	# get all possible relas by checking the concept's TTY against our mapping
	ttys = rxhandle.lookup_tty(rxcui)
	desired_relas = set()
	for tty in ttys:
		if tty in mapping:
			desired_relas.update(mapping[tty])
	if 0 == len(desired_relas):
		return
	
	# get all related rxcuis with the possible "rela" value(s)
	# Note: I had a "... AND rela IN (...)" in the following statement, but it
	# turns out just doing this in Python isn't slower and code is shorter
	rel_sql = 'SELECT DISTINCT rxcui1, rela FROM rxnrel WHERE rxcui2 = ?'
	for res in rxhandle.fetchAll(rel_sql, [rxcui]):
		if res[1] in desired_relas:
			storeVAs(rxhandle, res[0], vas, rxcui, res[1], at_level+1)

def storeVAs(rxhandle, rxcui, vas, from_rxcui, via_rela, level=0):
	""" Stores the drug classes `vas` for the given concept id, checking first
	if that concept already has classes and updating the set.
	"""
	assert(rxcui)
	assert(len(vas) > 0)
	
	# do we already have classes?
	exist_sql = 'SELECT va FROM va_cache WHERE rxcui = ?'
	exist_ret = doQ(rxhandle, exist_sql, [rxcui])
	if exist_ret and len(exist_ret) > 0:
		
		# bail out if we already have a class (!!!)
		return
		
		# split existing classes, decide if we all have them and if not, update
		exist_vas = set(exist_ret[0].split('|'))
		if vas <= exist_vas:
			return
		vas |= exist_vas
	
	# new, insert
	ins_sql = 'INSERT OR REPLACE INTO va_cache (rxcui, va, from_rxcui, rela, level) VALUES (?, ?, ?, ?, ?)'
	ins_val = '|'.join(vas)
	rxhandle.execute(ins_sql, (rxcui, ins_val, from_rxcui, via_rela, level))

def toDrugClasses(rxhandle, rxcui):
	sql = 'SELECT va FROM va_cache WHERE rxcui = ?'
	res = rxhandle.fetchOne(sql, (rxcui,))
	return res[0].split('|') if res is not None else []


def runImport(doc_handler=None):
	""" Run the actual linking.
	
	You can provide a :class:`DocHandler` subclass which will handle the JSON
	documents, for example store them to MongoDB for the MongoDocHandler. These
	classes are defined in `rxnorm_link_run.py` for now.
	"""
	
	# install keyboard interrupt handler
	def signal_handler(signal, frame):
		print("\nx>  Aborted")
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	
	# prepare RxNorm databases
	try:
		RxNorm.check_database()
		rxhandle = RxNormLookup()
		rxhandle.prepare_to_cache_classes()
	except Exception as e:
		logging.error(e)
		sys.exit(1)
	
	# fetch rxcui's for drug-type concepts (i.e. restrict by TTY)
	drug_types = ('SCD', 'SCDC', 'SBDG', 'SBD', 'SBDC', 'BN', 'SBDF', 'SCDG', 'SCDF', 'IN', 'MIN', 'PIN', 'BPCK', 'GPCK')
	param = ', '.join(['?' for d in drug_types])
	all_sql = "SELECT RXCUI, TTY from RXNCONSO where SAB='RXNORM' and TTY in ({})".format(param)
	
	all_drugs = rxhandle.fetchAll(all_sql, drug_types)
	num_drugs = len(all_drugs)
	
	# traverse VA classes; starts the VA drug class caching process if needed,
	# which runs a minute or two
	if rxhandle.can_cache():
		initVA(rxhandle)
		traverseVA(rxhandle, rounds=5, expect=num_drugs)
	
	# loop all concepts
	i = 0
	w_ti = 0
	w_va = 0
	w_either = 0
	last_report = datetime.now()
	print('->  Indexing {} items'.format(num_drugs))
	
	for res in all_drugs:
		params = [res[0]]
		params.extend(drug_types)
		label = rxhandle.lookup_rxcui_name(res[0])				# fast (indexed column)
		ndc = rxhandle.ndc_for_rxcui(res[0])					# fast (indexed column)
		ndc = RxNorm.ndc_normalize_list(ndc)			        # fast (string permutation)
		
		# find ingredients, drug classes and more
		ingr = toIngredients(rxhandle, [res[0]], res[1])		# rather slow
		ti = toTreatmentIntents(rxhandle, ingr, 'IN')			# requires "ingr"
		va = toDrugClasses(rxhandle, res[0])					# fast, loads from our cached table
		gen = toBrandAndGeneric(rxhandle, [res[0]], res[1])		# fast
		comp = toComponents(rxhandle, [res[0]], res[1])			# fast
		mech = toMechanism(rxhandle, ingr, 'IN')				# fast
		
		# create JSON-ready dictionary (save space by not adding empty properties)
		d = {
			'rxcui': res[0],
			'tty': res[1],
			'label': label,
		}
		if len(ndc) > 0:
			d['ndc'] = list(ndc)
		
		if len(ingr) > 0:
			d['ingredients'] = list(ingr)
		if len(ti) > 0:
			d['treatmentIntents'] = list(ti)
		if len(va) > 0:
			d['drugClasses'] = list(va)
		if len(gen) > 0:
			d['generics'] = list(gen)
		if len(comp) > 0:
			d['components'] = list(comp)
		if len(mech) > 0:
			d['mechanisms'] = list(mech)
		
		# count
		i += 1
		if len(ti) > 0:
			w_ti += 1
		if len(va) > 0:
			w_va += 1
		if len(ti) > 0 or len(va) > 0:
			w_either += 1
		
		# The dictionary "d" at this point contains all the drug's precomputed
		# properties, to debug print this:
		#print(json.dumps(d, sort_keys=True, indent=2))
		if doc_handler:
			doc_handler.addDocument(d)
		
		# log progress every 2 seconds or so
		if (datetime.now() - last_report).seconds > 2:
			last_report = datetime.now()
			print('-->  {:.1%}   n: {}, ti: {}, va: {}, either: {}'.format(i / num_drugs, i, w_ti, w_va, w_either), end="\r")
	
	# loop done, finalize
	if doc_handler:
		doc_handler.finalize()
	
	print('-->  {:.1%}   n: {}, ti: {}, va: {}, either: {}'.format(i / num_drugs, i, w_ti, w_va, w_either))
	print('->  Done')


if '__main__' == __name__:
	logging.basicConfig(level=logging.INFO)
	logging.warn('''  Running linking without document handler, meaning no RxNorm document will be stored.
               Adjust and run `rxnorm_link_run.sh` for more control.''')
	runImport()
