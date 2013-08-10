# -*- coding: utf-8 -*-

class Place:
	def __init__(self, name, background):
		self.name = name
		self.background = background

places = dict([
	('test.tmx', Place("학원", "gakuen.png"))
])

