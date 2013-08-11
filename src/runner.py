# -*- coding: utf-8 -*-

import item
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

class GameRunner(Runner):
	def __init__(self, loveee, heroine, place, dialog):
		self.loveee  = loveee
		self.heroine = heroine
		self.place   = place
		self.dialog  = dialog
		
		self.dialog.lock = True
		
	def end(self):
		self.dialog.lock    = False
		self.dialog.visable = False

	def narr(self, s):
		self.dialog.setMessage({"msgList" : [s]})

	def conv(self, s):
		if isinstance(s.name, script.Self):
			name = self.heroine.name
			engname = self.heroine.engname
		else:
			name = s.name
			engname = s.engname

		self.dialog.setMessage({"msgList" : [name + u":\t" + s.text], "image" : engname + ".png"})

	def choice(self, s):
		self.dialog.setChoices({
			"question" : u"선택지 : " + s.question,
			"choices" : s.selections
			})

		return 0

	def take(self, s):
		self.loveee.player.items.append(item.get_item(s.name))
		self.dialog.setMessage({"msgList" : [s.name + u"을 받았다!"]})

	def give(self, s, scr):
		if not self.loveee.player.items:
			return scr
			
		inventory = list()
		
		for i in self.loveee.player.items:
			if i.name in scr:
				inventory.append(script.Selection(i.name, s.script[i.name]))
			else:
				inventory.append(script.Selection(i.name, s.script[None]))
			
		self.dialog.setChoices({
			"question" : u"무엇을 줄까",
			"choices" : inventory
		})
		
		self.dialog.item_selection = True

	def love(self, s):
		self.heroine.love += s.val
		
	def route(self, s):
		i = s.var(self.loveee, self.heroine, self.place)
		
		return i