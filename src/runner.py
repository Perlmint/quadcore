# -*- coding: utf-8 -*-

import os

import item
import script
import dialog

import pygame

import inputBox

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
        
    def money(self, s):
        pass

class GameRunner(Runner):
    def __init__(self, loveee, heroine, place, dialog, world):
        self.loveee  = loveee
        self.heroine = heroine
        self.place   = place
        self.dialog  = dialog
        self.world   = world
        
        self.dialog.lock = True
        
    def end(self):
        print "end"
    
        self.dialog.lock    = False
        self.dialog.visable = False
        self.dialog.resetBox()
        
        pygame.mixer.music.stop()

    def narr(self, s):
        self.dialog.setMessage({"msgList" : [s]})

    def conv(self, s):
        self.dialog.lock = True
        if isinstance(s.name, script.Self):
            name = self.heroine.name
            engname = self.heroine.engname
        else:
            name = s.name
            engname = s.engname

        self.dialog.setMessage({"msgList" : [name + u":\t" + s.text], "image" : engname + ".png"})

    def choice(self, s):
        self.dialog.lock = True
        self.dialog.setMessage({"msgList" : [""]})
        self.dialog.setChoices({
            "question" : u"선택지 : " + s.question,
            "choices" : s.selections
            })
            
        print "choice"

        return 0

    def hide(self, s):
        self.dialog.removePersonImage()

    def take(self, s):
        self.dialog.lock = True
        self.loveee.player.items.append(item.get_item(s.name))
        self.dialog.setMessage({"msgList" : [s.name + u"을 받았다!"]})

    def give(self, s, scr):
        self.dialog.lock = True
        if not self.loveee.player.items and not script.Money in s.script:
            return scr
            
        print "ttt"
            
        inventory = list()
        
        if script.Money in s.script:
            inventory.append(script.Selection(u"돈", s.script[script.Money]))
        
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
        self.dialog.lock = True
        self.heroine.love += s.val
        
    def route(self, s):
        self.dialog.lock = True
        i = s.var(self.loveee, self.heroine, self.place, s)
        
        return i
        
    def bgm(self, s):
        pygame.mixer.music.load(os.path.join('..', 'bgm', s.name))
        pygame.mixer.music.play(-1)
        
    def se(self, s):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        file = os.path.join('..', 'se', s.name)
        print file
        pygame.mixer.Sound(file).play()
        
    def money(self, s):
        print "ask!!!!!!!!!!!!"
        val = inputBox.ask(self.world.screen, s.query)
        print val
        return s.callback(int(val))
        