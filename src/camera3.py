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
# Name:        camera3.py
# Purpose:     calculate relating coordinate
#
# Author:      MuychivTaing
#
# Created:     19/02/2012
# Copyright:   (c) MuychivTaing 2012
# Licence:     GPL v3
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
import os
from random import randint

class Camera(object):

    def __init__(self):
        self.cordX = 0
        self.cordY = 0
        self.windowX = 80
        self.windowY = 80
        self.dx = 0
        self.dy = 0

        self.world = None

        self.follow = None      #the target that camera will move with

    def addWorld(self, world):
        self.world = world
        self.map_size_x = world.map.tmxMap.width * 32
        self.map_size_y = world.map.tmxMap.height * 32
        self.tile_pos_list = world.map.posList

    def translate(self, rect):
        return rect.move(-self.cordX, -self.cordY)

    def update(self):
        self.dx = self.follow.speed
        self.dy = self.follow.speed

        translatedRect = self.translate(self.follow.rect)
        if translatedRect.left <= self.windowX:
            self.cordX -= self.dx
        elif translatedRect.right >= 640 - self.windowX:
            self.cordX += self.dx
        if translatedRect.top <= self.windowY:
            self.cordY -= self.dy
        elif translatedRect.bottom >= 480 - self.windowY:
            self.cordY += self.dy

        self._check_bounder()

    def render1(self, surface):
        top = self.cordY/32
        bottom = (480+self.cordY)/32 + 1
        left = self.cordX/32
        right = (640+self.cordX)/32 + 1

        if top < 0: top =0
        if left < 0: left = 0
        for tile_y in self.tile_pos_list[top:bottom]:
            for tile_x in tile_y[left:right]:
                imageLayer1 = self.map.getImage(tile_x[0]/32, tile_x[1]/32, 0)
                imageLayer2 = self.map.getImage(tile_x[0]/32, tile_x[1]/32, 1)
                if imageLayer1:
                    #this no image at this location so skip it
                    surface.blit(imageLayer1,
                            (tile_x[0]-self.cordX, tile_x[1]-self.cordY))
                if imageLayer2:
                    #this no image at this location so skip it
                    surface.blit(imageLayer2,
                            (tile_x[0]-self.cordX, tile_x[1]-self.cordY))

    def render(self, surface, worldMap, layer):
        top = self.cordY/32
        bottom = (480+self.cordY)/32 + 1
        left = self.cordX/32
        right = (640+self.cordX)/32 + 1
	if bottom > worldMap.size[1]:
		bottom = worldMap.size[1]

	if right > worldMap.size[0]:
		right = worldMap.size[0]


        if top < 0: top =0
        if left < 0: left = 0
        for tile_y in self.tile_pos_list[top:bottom]:
            for tile_x in tile_y[left:right]:
                image = worldMap.getImage(tile_x[0]/32, tile_x[1]/32, layer)

                if image:
                    #this no image at this location so skip it
                    surface.blit(image,
                            (tile_x[0]-self.cordX, tile_x[1]-self.cordY))

    def move(self, direction):
        if direction == "up":
            if self.dy > 0:
                self.dy = 0
            self.vpY += self.dy
        elif direction == "down":
            if self.dy < 0:
                self.dy = 0
            self.vpY += self.dy
        if direction == "left":
            if self.dx > 0:
                self.dx = 0
            self.vpX += self.dx
        elif direction == "right":
            if self.dx < 0:
                self.dx = 0
            self.vpX += self.dx

    def set_follow(self, sprite):
        rect = pygame.Rect(0,0,640,480)     #640 and 480 is the screen size and should be able to change
        self.follow = sprite
        rect.center = self.follow.rect.center
        self.cordX, self.cordY = rect.topleft

    def _check_bounder(self):
        if self.cordX < 0:
            self.cordX = 0
##            self.dx = 0
        elif self.cordX > self.map_size_x - 640:
            self.cordX = self.map_size_x - 640
##            self.dx = 0
        if self.cordY < 0:
            self.cordY = 0
##            self.dy = 0
        elif self.cordY > self.map_size_y - 480:
            self.cordY = self.map_size_y - 480
##            self.dy = 0

