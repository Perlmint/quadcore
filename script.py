# -*- coding: utf-8 -*-

class Selection:
	def __init__(self, name, script):
		self.name   = name
		self.script = script

class Choice:
	def __init__(self, question, selections):
		self.question   = question
		self.selections = selections

class EndScript:
	pass

class CallbackScript:
	def __init__(self, callback):
		self.callback = callback

die_script = [
	"푹찍",
	EndScript(),
]

test = [
	"나는 너가 좋아",
	"그러니 죽어주면 좋겠어",
	Choice("죽을까", [
		Selection("죽는다", die_script),
		Selection("도망간다", die_script),
	])
]

