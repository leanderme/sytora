#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#	Draw an RxNorm graph for a given RxCUI.
#	You must have "dot" installed (Graphviz)
#
#	2014-02-18	Created by Pascal Pfiffner

import sys
import subprocess

from rxnorm import RxNormCUI
from graphable import GraphvizGraphic


if '__main__' == __name__:
	rxcui = sys.argv[1] if 2 == len(sys.argv) else None
	if rxcui is None:
		print('x>  Provide a RXCUI as first argument')
		sys.exit(0)
	
	rx = RxNormCUI(rxcui)
	gv = GraphvizGraphic('rxgraph.pdf')
	gv.out_dot = 'rxgraph.dot'
	gv.max_depth = 8
	gv.max_width = 15
	
	gv.write_dot_graph(rx)
	
	print('->  DOT file:   {}'.format(gv.out_dot))
	print('->  PNG graph:  {}'.format(gv.out_file))
	
	subprocess.call(['open', gv.out_file])
