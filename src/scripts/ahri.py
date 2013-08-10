# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from script import *

def TestFunc(loveee, heroine, place):
	if heroine.love == 0:
		heroine.love = 100
		return 0

	return 1

die_script = [
	Conversation(Self(), u"푹찍"),
	Conversation(Self(), u"아잉"),
	EndScript()
]

live_script = [
	Conversation(Self(), u"그래 도망가 봐 호호"),
	Route("Test", TestFunc,
	[
		[Conversation(Self(), u"이번엔 봐주지만 다음에 만나면 죽을테니!"), EndScript()],
		[Conversation(Self(), u"귀여워서 봐준다♥"), EndScript()],
	]),
]

script = [
	Conversation(Self(), u"너는 죽었어♥"),
	Choice(u"죽을까", [
		Selection(u"죽는다", die_script),
		Selection(u"도망간다", live_script)
		]),

	EndScript()
]

script.append(EndScript())