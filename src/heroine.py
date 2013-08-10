# -*- coding: utf-8 -*-

import script

class Heroine:
	def __init__(self, name, engname, global_scr, local_scr, theme):
		self.name	= name
		self.engname = engname
		self.global_scr	= global_scr
		self.local_scr	= local_scr
		self.theme      = theme

		self.love = 0

		self.status = "none"
	def setWorld(self, world):
		self.world = world

heroines = dict([
	("h1", Heroine(u"사이온지 세카이", "sekai", [script.sekai], {
		u"학원" : [script.test],
	}, None))
])
