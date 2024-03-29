# -*- coding: utf-8 -*-

from item import get_items

import heroine
import place
import script

import random

import os
import pygame

import conch

items = get_items()

class Player:
    def __init__(self, name):
        self.name = name

        self.balance = 100000
        self.items   = list()

class LoveEE:
    def __init__(self, player):
        self.player = player
        
        self.jukebox = conch.Jukebox()
        
        pygame.mixer.music.load(os.path.join('..', 'bgm', "bgm.ogg"))
        pygame.mixer.music.play(-1)

    def select_place(self, runner):
        ss = list()

        for i in place.places:
            ss.append(script.Selection(i.name, None))

        c = script.Choice("어디로 갈까?", ss)

        r = runner(self, heroine.Heroine("장소 선택", None, None, None), None)

        return r.choice(c)


    def run(self, runner, scr):
        res = self.select_place(runner)

        p = place.places[res]

        r = random.randrange(len(heroine.heroines))

        h = heroine.heroines[r]

        s = scr

        i = script.ScriptInterpreter(s)

        while i.run(runner(self, h, p)):
            pass

        
