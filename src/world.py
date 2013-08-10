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
# Name:        world.py
# Purpose:     Managing entities in the game so they can interact with each other
#              if needed.
# Author:      MuychivTaing
#
# Created:     16/02/2012
# Copyright:   (c) MuychivTaing 2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import dialog
import os
from map import Map
import npc
import sprite
from camera3 import Camera
import character.spriteinfo as spriteinfo
import random

class World(object):
    currentWorld = None

    def __init__(self, worldFileName = None):
        World.currentWorld = self
        #define world attribute
        self.entities= []
        self.camera= None
        self.map = None
        self.player = None
        self.dialog = dialog.DialogBox()
        self.cleanup = False
        if worldFileName is not None:
            self.loadWorldFile(worldFileName)

    def getPlayername(self):
        return self.loveee.player.name

    def loadWorldFile(self, worldName):
        if worldName is None:
            raise Exception("world file name is none")
	_map = __import__('maps.%s' % worldName, fromlist=['*'])

        self.cleanup = True
	while len(self.entities) > 0:
		self.killEntity(self.entities[0])

        # map
	worldMap = Map()
	worldMap.load(os.path.join("..", "map", _map.map['filename']), _map.map['filename'])
        self.addMap(worldMap)

	# event
        for event in _map.event:
            eventEntity = npc.Event(event['action'])
            #eventEntity.load_sprite_sheet(os.path.join("..", "graphics", "System", "collision.png"), (32,32), (0,0), (32,32))
            eventEntity.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor2.png"), (32,32), (0,0), (96,128))
            eventEntity.set_pos(event['pos'][0], event['pos'][1])
#            eventEntity.action = lambda:
            self.addEntities(eventEntity)

        for heroine in _map.heroine:
            if random.random() < heroine['probability']:
                newHeroine = npc.Npc(heroine['name'])
                newHeroine.load_sprite_sheet(spriteinfo.heroine[heroine['name']]["sprite"], spriteinfo.heroine[heroine['name']]["size"], spriteinfo.heroine[heroine['name']]["startpos"], spriteinfo.heroine[heroine['name']]["sheetsize"])
                newHeroine.speed_is(3)
                newHeroine.walking_boundary_is(worldMap.size[0], worldMap.size[1])
                newHeroine.set_pos(random.uniform(0, worldMap.size[0]), random.uniform(0, worldMap.size[1]))
                self.addEntities(newHeroine)

	# player
        player = sprite.Hero()
        player.load_sprite_sheet(spriteinfo.player["sprite"], spriteinfo.player["size"], spriteinfo.player["startpos"], spriteinfo.player["sheetsize"])
        player.speed_is(3)
        player.walking_boundary_is(worldMap.size[0], worldMap.size[1])
        player.set_pos(_map.player['pos'][0], _map.player['pos'][1])
        self.addEntities(player)
        cam = Camera()
        cam.set_follow(player)
        self.setCamera(cam)

    def addMap(self, map):
        """specify the map
           Currently use r collision detection
        """
        self.map = map

    def addPlayer(self, player):
        self.player = player
        player.world = self

    def setCamera(self, camera):
        """specify the camera that game is going to use
           to render the world
        """
        self.camera = camera
        camera.addWorld(self)

    def render(self, surface):
        """use the spesify camera to render all the entities onto the surface.
           Camera has to be set before usage.
        """
        #check if there is no camera is set, then do nothing
        if not (self.camera):
            print("No camera!")
            return

        #check the availibility of entities in the world    
        if not self.entities:
            print("No entities to render")
            return

        if self.cleanup:
            surface.fill((0,0,0))
            self.cleanup = False
        #rendering entities according to camera cordinate
        #assuming background layer is index 0
        self.camera.render(surface, self.map, 0)
##        surface.blit(self.player.image, self.camera.translate(self.player.rect))
        for entity in self.entities:
            if entity.__class__.__name__ == "Event":
                continue
            #check to render only the entities that is visible
            translatedRect = self.camera.translate(entity.rect)
            if (translatedRect.left <= -32 or translatedRect.right >= 672 or translatedRect.top <= -32 or
                translatedRect.bottom >= 512):
                continue
            surface.blit(entity.image, self.camera.translate(entity.rect))


        #after bliting all entities in the world, we blit the over layer on the top
        for layerIndex in xrange(1, len(self.map.tmxMap.layers)):
            if self.map.tmxMap.layers[layerIndex].name in ["collision", "over"]:
                continue
            self.camera.render(surface, self.map, layerIndex)

##        if self.dialog.visable:
        self.dialog.draw(surface)

    def update(self):
        """ update all the entity in the world
        """
        if self.player:
            self.player.update()
        #check for any enities or update will be error
        if self.entities:
            for entity in self.entities:
                #check to update only the entities that is visible
                if self.camera:
                    translatedRect = self.camera.translate(entity.rect)
                    if (translatedRect.left <= -32 or translatedRect.right >= 832 or translatedRect.top <= -32 or
                        translatedRect.bottom >= 632):
                        continue
                entity.update()
        if self.camera:
            self.camera.update()

##        if self.dialog.visable:
        self.dialog.update()

    def addEntities(self, entity):
        """ entity to add to the world
            entity should be a sprite class type
        """
        self.entities.append(entity)
        entity.world = self

    def killEntity(self, entity):
        """ Entity to remove from the world
            entity should be a sprite class type
        """
        #remove the entities if the entity is in the world
        if entity in self.entities:
            self.entities.remove(entity)
