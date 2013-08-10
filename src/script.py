# -*- coding: utf-8 -*-

import item
import copy

class Self:
	pass

class Money:
	def __init__(self, value):
		self.value = value

class Route:
	def __init__(self, name, var, scripts):
		self.name   = name
		self.var    = var
		self.scripts = scripts

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
	def __init__(self, item):
		self.item = item

class Give:
	def __init__(self, var):
		self.var = var

class Love:
	def __init__(self, val):
		self.val = val

class BGM:
	def __init__(self, name):
		self.name = name

class SE:
	def __init__(self, name):
		self.name = name


class ScriptInterpreter:
	def __init__(self, script):
		self.script = copy.deepcopy(script)
	
	def run(self, runner):
		if not self.script:
			return False
			
		s = self.script.pop(0)

		if isinstance(s, (str, unicode)):
			runner.narr(s)	
		elif isinstance(s, Conversation):
			runner.conv(s)
		elif isinstance(s, Choice):
			res = runner.choice(s)
		elif isinstance(s, EndScript):
			runner.end()
			self.script = None
			return False
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
		elif isinstance(s, Route):
			res = runner.route(s)
			self.script = s.scripts[res]

			self.run(runner)
		elif isinstance(s, Love):
			runner.love(s)
		elif isinstance(s, BGM):
			runner.bgm(s)
		elif isinstance(s, SE):
			runner.se(s)

		return True
