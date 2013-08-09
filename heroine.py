# -*- coding: utf-8 -*-

import script

class Heroine:
	def __init__(self, name, global_scr, local_scr):
		self.name	= name
		self.global_scr	= global_scr
		self.local_scr	= local_scr

heroines = [
	Heroine("은로리", [script.test], [script.test])
]

