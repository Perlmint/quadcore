# -*- coding: utf-8 -*-

class Item:
	def __init__(self, name, price):
		self.name  = name
		self.price = price

items = [
	Item("아이템",	1000),
	Item("뷁",	2000),
]

def get_items():
	ret = dict()

	for i in items:
		ret[i.name] = i

	return ret

