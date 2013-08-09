# -*- coding: utf-8 -*-

import script

class Runner:
	def narr(self, s):
		pass

	def conv(self, s):
		pass

	def choice(self, s):
		return 0

	def end(self):
		pass

	def callback(self, s):
		s.callback(s.data)
		pass

	def show(self, s):
		pass

	def hide(self, s):
		pass

	def back(self, s):
		pass

	def take(self, s):
		pass

	def give(self, s):
		return s

	def route(self, s):
		return 0

class CliRunner(Runner):
	def __init__(self, name):
		self.name = name

	def narr(self, s):
		print s
		raw_input()

	def conv(self, s):
		if isinstance(s.name, script.Self):
			name = self.name
		else:
			name = s.name

		print name + ":\t" + s.text
		raw_input()

	def choice(self, s):
		print "선택지: " + s.question
		print

		no = 0

		for i in s.selections:
			print "%d %s" % (no, i.name)
			no += 1

		return input("선택: ")

t = script.ScriptInterpreter(script.test)
runner = CliRunner("히로인")

while t.run(runner):
	pass


