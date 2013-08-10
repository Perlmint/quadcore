# -*- coding: utf-8 -*-
import sys
sys.path.append("scripts")

import sekai
import ahri

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

scripts = {
	"sekai" : sekai.script,
	"ahri" : ahri.script
}

heroineCharacters = {
	"sekai" : Heroine(u"사이온지 세카이", "sekai", [sekai.script], {
		u"학원" : None,
	}, None),
	"ahri" : Heroine(u"아리", "ahri", [ahri.script], {
		u"학원" : None,
	}, None)
}

sekai.heroine = heroineCharacters["sekai"]
ahri.heroine = heroineCharacters["ahri"]

heroines = dict([
	("sekai", heroineCharacters["sekai"]),
	("ahri", heroineCharacters["ahri"])
	])