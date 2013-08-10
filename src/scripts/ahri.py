# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from script import *
import pygame

def LiveOrLive(loveee, heroine, place):
	if heroine.love <= 100:
		heroine.love = heroine.love + 50
		return 0

	return 1

def DieRightAway(loveee, heroine, place):
	if heroine.love < 0:
		return 1
	else:
		return 0

def GameOver(data):
	pygame.quit()
	pass

die_script = [
	Conversation(Self(), u"푹찍"),
	Conversation(Self(), u"아잉"),
	Love(-10),
	EndScript()
]

live_script = [
	Route("Test", LiveOrLive,
	[
		[Conversation(Self(), u"그래 도망가 봐 호호"), Conversation(Self(), u"이번엔 봐주지만 다음에 만나면 죽을테니!"), EndScript()],
		[Conversation(Self(), u"귀여워서 봐준다♥"), EndScript()],
	]),
]

script = [
	Route("Dead End", DieRightAway,
	[
		[Conversation(Self(), u"너는 죽었어♥"),
			Choice(u"죽을까", [
				Selection(u"죽는다", die_script),
				Selection(u"도망간다", live_script)
				]),

			EndScript()
		],
		[
			Conversation(Self(), u"죽어!!"),
			CallbackScript(GameOver, None)
		]
	])
]

script.append(EndScript())