# -*- coding: utf-8 -*-

class Self:
	pass

class Money:
	def __init__(self, value):
		self.value = value

class Route:
	def __init__(self, name, var, script):
		self.name   = name
		self.var    = var
		self.script = script

class Conversation:
	def __init__(self, name, text):
		self.name = name
		self.text = text

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
	def __init__(self, callback, data):
		self.callback = callback
		self.data = data

class ShowHeroine:
	def __init__(self, image):
		self.image = image

class HideHeroine:
	def __init__(self, image):
		self.image = image

class Background:
	def __init__(self, image):
		self.image = image

class Take:
	def __init__(self, name, item):
		self.name = name
		self.item = item

class Give:
	def __init__(self, var):
		self.var = var

class Routing:
	def __init__(self, name, routes):
		self.name   = name
		self.routes = routes


class ScriptInterpreter:
	def __init__(self, script):
		self.script = script
	
	def run(self, runner):
		if not self.script:
			return False

		s = self.script.pop(0)

		if isinstance(s, str):
			runner.narr(s)
		elif isinstance(s, Conversation):
			runner.conv(s)
		elif isinstance(s, Choice):
			res = runner.choice(s)

			self.script = s.selections[res].script
		elif isinstance(s, EndScript):
			runner.end()
			self.script = list()
		elif isinstance(s, CallbackScript):
			runner.callback(s)
		elif isinstance(s, ShowHeroine):
			runner.show(s)
		elif isinstance(s, HideHeroine):
			runner.hide(s)
		elif isinstance(s, Background):
			runner.back(s)
		elif isinstance(s, Take):
			runner.take(s)
		elif isinstance(s, Give):
			self.script = runner.give(s, self.script)
		elif isinstance(s, Routing):
			res = runner.route(s)

			self.script = s.routes[res].script

		return True


die_script = [
	"푹찍",
	EndScript(),
]

live_script = [
	"도망",
	EndScript(),
]

test = [
	Background(Self()),
	Conversation(Self(), "나는 너가 좋아"),
	Conversation(Self(), "그러니 죽어주면 좋겠어"),
	"죽어야 하나 고민이네",
	Choice("죽을까", [
		Selection("죽는다", die_script),
		Selection("도망간다", live_script),
	])
]

