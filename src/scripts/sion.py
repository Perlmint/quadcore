# -*- coding: utf-8 -*-
from script import *

def init_route(loveee, heroine, place, self):
	print heroine.love
	
	if heroine.love < 100000:
		heroine.love += 100000
	
	return 0
	
p = []
	
main_route = [
	[
		Choice(u"뭐하고 놀까?", [
		])
	]
]

script = [
	Conversation(Self(), u"안녕"),
	Conversation(Self(), u"오랫만이야"),
	Route(None, init_route, main_route)
]