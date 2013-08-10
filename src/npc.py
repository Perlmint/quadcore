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
import script
import runner
import heroine, random, place

class Event(sprite.Npc):
    def __init__(self):
        super(Event, self).__init__()
        self.movement_x = self.movement_y = self.speed = 0
        self.direction_change_frq = 0 
        self.current_frequency = 0

    def action(self):
        pass

class Npc(sprite.Npc):
    def __init__(self, name = "None"):
        super(Npc, self).__init__()
        self.name = name
        self.category = "npc"
        self.current_frequency = 60
        self.movement_x = self.movement_y = self.speed = 2

    def action(self, scr = None):
        h = heroine.heroines[self.name]
        p = place.places[self.world.map.name]
        
        if not scr:
            scr = h.global_scr[0]
        
        i = script.ScriptInterpreter(scr)
        r = runner.GameRunner(self.world.loveee, h, p, self.world.dialog)
        
        def doit():
            print "wahaha"
            ret = i.run(r)
            if not ret:
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
        if self.walking_mode == 2:
            return
        seed = random.random()
        if seed < 0.05:
          self.set_walking_mode(1 if self.walking_mode == 0 else 0)
        if self.walking_mode == 0:
          return
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
        self.move(self.current_direction)

    def direction_handling(self):
        pass
