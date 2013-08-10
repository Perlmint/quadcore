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
# Name:        main.py
# Purpose:     The entry file for game
#
# Author:      MuyChiv Taing
#
# Created:     09/03/2012
# Copyright:   Copyright MuyChiv Taing 2012
# Licence:     GPL v3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import game
import pygame
import world

import loveee

##class Main(game.Game):
##    def __init__(self):
##        super(Main, self).__init__()
##        npc1 = npc.MyRpg()
##        self.world.addEntities(npc1)
##        camera = camera3.Camera()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Team - quadcore")

    clock = pygame.time.Clock()
    keepGoing = True

    gameWorld = world.World('town')
	
    p = loveee.Player(u"플레이어")
    gameWorld.loveee = loveee.LoveEE(p)
    
    while keepGoing:
        clock.tick(32)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                keepGoing = False

        gameWorld.update()
        gameWorld.render(screen)
        pygame.display.flip()

    pygame.quit()
