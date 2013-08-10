# -*- coding: utf-8 -*-

from script import *

script = [
	Conversation(Self(), u""),
	Choice(u"죽을까", [
		Selection(u"죽는다", die_script),
		Selection(u"도망간다", live_script)
		]),
    	EndScript()
]