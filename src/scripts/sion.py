# -*- coding: utf-8 -*-
from script import *

import random
import pygame

import item

def niceboat_route(loveee, heroine, place, self):
	pygame.quit()
	exit()
	
	return 0

def init_route(loveee, heroine, place, self):
	print heroine.love
	
	if heroine.love < 100000:
		heroine.love += 100000
	
	return 0
	
def random_route(loveee, heroine, place, self):
	return random.randint(0, len(self.scripts) - 1)
	
niceboat = [
	SE("scream_echo.ogg"),
	u"Nice Boat",
	Route(None, niceboat_route, [[EndScript()]])
]
	
h_hug = [
	Conversation(Self(), u"나를...안아줘..."),
	Conversation(Self(), u"몸이...뜨거워..."),
	u"푹찍",
	Conversation(Self(), u"이제.. 계속 나와 함께 있을 수 있어")
]

h_undress = [
	Conversation(Self(), u"옷을 벗겨주지 않을래?"),
	Conversation(Self(), u"이쪽으로 와줘"),
]

give_scr = [
	Conversation(Self(), u"고마워"),
	Conversation(Self(), u"이건 내 답례야"),
	u"푹찍",
] + niceboat

def give_route(loveee, heroine, place, self):
	if not loveee.player.items:
		self.scripts = [[u"줄 선물이 없다"]]
	else:
		self.scripts = [[Give(None, dict([(None, give_scr)]))]]
		
	return 0
	

give_present = [
	Route(None, give_route, [])
]

def take_route(loveee, heroine, place, self):
	self.scripts = [[
		Take(random.choice(item.items).name)
	]]
	
	return 0

take_present = [
	Route(None, take_route, [])
]

heart = [
	u"♡♡♡",
	Route(None, random_route, [
		h_hug + niceboat,
		h_undress + niceboat
	])
]
	
main_route = [
	[
		Choice(u"뭐하고 놀까?", [
			Selection(u"선물을 준다",  give_present),
			Selection(u"선물을 받는다", take_present),
			Selection(u"♡", heart),
		])
	]
]

script = [
	Conversation(Self(), u"안녕"),
	Conversation(Self(), u"오랫만이야"),
	Conversation(Self(), u"심심해"),
	Conversation(Self(), u"놀자"),
	Route(None, init_route, main_route)
]