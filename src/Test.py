# -*- coding: UTF-8 -*-

import sys
from heroine import Heroine

class TestHeroine(Heroine):
	def __init__(self, name):
		Heroine.__init__(self, name)

		self.messageMap = {
			"default" : {
				"messages" : [
					["Hi", "cat.gif"],
					["LoL", None]
					],
				"menu" : [
					[u"안녕~  뭐 하니", "boo"],
					[u"무한루프다 하하하하", "default"]
				]
			},

			"boo" : {
				"messages" : ["boo", "boo2"]
			}
		}

		def callback_default():
			self.love = 0

		self.callbackMap = {
			"default" : "callback_default"
		}