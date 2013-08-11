# -*- coding: utf-8 -*-

class Item:
	def __init__(self, name, price):
		self.name  = name
		self.price = price

items = [
	Item(u"아이템",	1000),
	Item(u"뷁",		2000),
	Item(u"가터벨트",	50000),
	Item(u"메이드복",	100000),
	Item(u"이상한 약",	100000000)
]

def get_items():
	ret = dict()

	for i in items:
		ret[i.name] = i

	return ret
	
def get_item(name):
	d = get_items()
	
	return d[name]

