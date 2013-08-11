# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
#   This file is part of University of Python
#   Foobar is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Foobar is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Name:        npc.py
# Purpose:     For creating npc with custom respond
#
# Author:      MuyChiv Taing
#
# Created:     09/03/2012
# Copyright:   Copyright MuyChiv Taing 2012
# Licence:     (C) Muychiv Taing
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sprite
import os
import sys
from script import *
import runner
import heroine, random, place, world
import pygame

class Event(sprite.Npc):
    def __init__(self, target):
        super(Event, self).__init__()
        self.movement_x = self.movement_y = self.speed = 0
        self.direction_change_frq = 0 
        self.current_frequency = 0
        self.target = target

    def action(self):
        world.World.currentWorld.loadWorldFile(self.target)

class Npc(sprite.Npc):
    def __init__(self, name, map):
        super(Npc, self).__init__()
        self.name = name
        self.map = map
        self.category = "npc"
        self.current_frequency = 60
        self.movement_x = self.movement_y = self.speed = 2
        self.h = heroine.heroineCharacters[self.name]
        self.boat_success = False
        self.boat_cooltime = 3000
        self.boat_chase_time = 0
        self.boat_last_time = 0

    def action(self, scr = None):
        p = place.places[self.world.map.name]

        if scr == None:
            scr = self.h.global_scr[0]
        
        i = ScriptInterpreter(scr)
        r = runner.GameRunner(self.world.loveee, self.h, p, self.world.dialog, self.world)
        
        def doit():
            ret = i.run(r)
            
            if isinstance(ret, Pass):
                return doit()
            
            if ret == False:
                self.set_walking_mode(0)
            
            return ret

        self.set_walking_mode(2)

        if not doit():
            return None
            
        return doit

    def set_walking_mode(self, mode):
        """
            mode = 0, 1, or 2

            0 is standstill, 1 is always walking, 2 is walking stop.
        """
        self.walking_mode = mode

    def other_update(self):
        if self.h.love >= 50:
            self.walking_mode = 3

        if self.walking_mode == 2:
            return
        seed = random.random()
        if seed < 0.05:
          self.set_walking_mode(1 if self.walking_mode == 0 else 0)
        if self.walking_mode == 0:
          return

        if self.walking_mode == 1:
            seed = random.random()
            direction = self.direction_list.index(self.current_direction)
            if seed < 0.03:
                direction = direction - 1
            elif seed < 0.06:
                direction = direction + 1
            if direction < 0:
                direction = 4 + direction
            if direction > 3:
                direction = direction - 4
            if self.direction_list.index(self.current_direction) != direction:
                self.current_direction = self.direction_list[direction]
        elif self.walking_mode == 3: #Nice boat
            player = world.World.currentWorld.player

            if player == None:
                return

            playerRect = player.rect

            xDiff = (playerRect.x - self.rect.x)
            yDiff = (playerRect.y - self.rect.y)

            if xDiff == 0:
                xDir = 0
            else:
                xDir =  xDiff / abs(xDiff)

            if yDiff == 0:
                yDir = 0
            else:
                yDir = yDiff / abs(yDiff)

            if xDir >= 0:
                xDirection = 2
            elif xDir < 0:
                xDirection = 0
            
            if yDir >= 0:
                yDirection = 3
            elif yDir < 0:
                yDirection = 1

            if abs(xDiff) >= abs(yDiff):
                direction = xDirection
            else:
                direction = yDirection

            if xDir == 0 and yDir == 0:
                pass

            self.current_direction = self.direction_list[direction]


        self.move(self.current_direction)

    def move(self, direction):
        super(Npc, self).move(direction)

        if self.walking_mode == 3 and self.boat_success == False:
            collideRect = (20,20)
            player = world.World.currentWorld.player

            if player == None:
                    return

            playerRect = player.rect

            xDiff = (playerRect.x - self.rect.x)
            yDiff = (playerRect.y - self.rect.y)

            if abs(xDiff) <= collideRect[0] and abs(yDiff) <= collideRect[1]:
                if self.boat_last_time == 0:
                    self.boat_last_time = pygame.time.get_ticks()
                    self.boat_chase_time = 0
                else:
                    currentTime = pygame.time.get_ticks()
                    self.boat_chase_time = self.boat_chase_time + currentTime - self.boat_last_time
                    self.boat_last_time = currentTime

                if self.boat_chase_time >= self.boat_cooltime:
                    player.action = self.action([Conversation(Self(), u"죽어!!!"), u"Game Over", CallbackScript(GameOver, None)])
                    self.boat_success = True
            else:
                self.boat_last_time = 0
                self.boat_chase_time = 0

    def direction_handling(self):
        pass
