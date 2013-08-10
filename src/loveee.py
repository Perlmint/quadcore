# -*- coding: utf-8 -*-

from item import get_items

import heroine
import place
import script

import random

items = get_items()

class Player:
	def __init__(self, name):
		self.name = name

		self.balance = 100000
		self.items   = list()

class LoveEE:
	def __init__(self, player):
		self.player = player

	def select_place(self, runner):
		ss = list()

		for i in place.places:
			ss.append(script.Selection(i.name, None))

		c = script.Choice("어디로 갈까?", ss)

		r = runner(self, heroine.Heroine("장소 선택", None, None, None), None)

		return r.choice(c)


	def run(self, runner):
		res = self.select_place(runner)

		p = place.places[res]

		r = random.randrange(len(heroine.heroines))

		h = heroine.heroines[r]

		s = h.global_scr[0]

		i = script.ScriptInterpreter(s)

		while i.run(runner(self, h, p)):
			pass

		
