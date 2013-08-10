# -*- coding: utf-8 -*-

import script
import dialog

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

	def give(self, s, script):
		return s

	def route(self, s):
		return 0

	def love(self, s):
		pass

	def bgm(self, s):
		pass

	def se(self, s):
		pass

class CliRunner(Runner):
	def __init__(self, loveee, heroine, place):
		self.loveee  = loveee
		self.heroine = heroine
		self.place   = place
		self.dialog = heroine.world.dialog

	def narr(self, s):
		print s
		dialog.setMessage({"msgList" : [s]})

	def conv(self, s):
		if isinstance(s.name, script.Self):
			name = self.heroine.name
		else:
			name = s.name

		self.dialog.setMessage({"msgList" : [name + u":\t" + s.text], "image" : "cat.gif"})

	def choice(self, s):
		print "선택지: " + s.question
		dialog.setMessage({"msgList" : [u"선택지: " + s.question]})

		no = 0

		for i in s.selections:
			print "%d %s" % (no, i.name)
			no += 1

		return input("선택: ")

	def take(self, s):
		print s.item.name + "을 받았다!"

	def give(self, s, script):
		if not self.loveee.player.items:
			print "줄 아이템이 없다"
			return script

		print "무엇을 줄까:"
		print

		no = 0

		for i in self.loveee.player.items:
			print "%d % " % (no, i.name)
			no += 1

		res = input("선택: ")

		return script

	def love(self, s):
		self.heroine.love += s.val

class GameRunner(Runner):
	def __init__(self, loveee, heroine, place, dialog):
		self.loveee  = loveee
		self.heroine = heroine
		self.place   = place
		self.dialog = dialog

	def narr(self, s):
		print s
		dialog.setMessage({"msgList" : [s]})

	def conv(self, s):
		if isinstance(s.name, script.Self):
			name = self.heroine.name
		else:
			name = s.name

		self.dialog.setMessage({"msgList" : [name + u":\t" + s.text], "image" : "cat.gif"})

	def choice(self, s):
		print "선택지: " + s.question
		dialog.setMessage({"msgList" : [u"선택지: " + s.question]})

		no = 0

		for i in s.selections:
			print "%d %s" % (no, i.name)
			no += 1

		return input("선택: ")

	def take(self, s):
		print s.item.name + "을 받았다!"

	def give(self, s, script):
		if not self.loveee.player.items:
			print "줄 아이템이 없다"
			return script

		print "무엇을 줄까:"
		print

		no = 0

		for i in self.loveee.player.items:
			print "%d % " % (no, i.name)
			no += 1

		res = input("선택: ")

		return script

	def love(self, s):
		self.heroine.love += s.val
