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

class World(object):

    def __init__(self):
        #define world attribute
        self.entities= []
        self.camera= None
        self.map = None
        self.player = None
        self.dialog = dialog.DialogBox()

    def addMap(self, map):
        """specify the map
           Currently use for collision detection
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

        #rendering entities according to camera cordinate
        #assuming background layer is index 0
        self.camera.render(surface, self.map, 0)
##        surface.blit(self.player.image, self.camera.translate(self.player.rect))
        for entity in self.entities:
            #check to render only the entities that is visible
            translatedRect = self.camera.translate(entity.rect)
            if (translatedRect.left <= -32 or translatedRect.right >= 672 or translatedRect.top <= -32 or
                translatedRect.bottom >= 512):
                continue
            surface.blit(entity.image, self.camera.translate(entity.rect))

        #after bliting all entities in the world, we blit the over layer on the top
        for layerIndex in xrange(1, len(self.map.tmxMap.layers)):
            if self.map.tmxMap.layers[layerIndex].name == "collision":
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
                    if (translatedRect.left <= -32 or translatedRect.right >= 672 or translatedRect.top <= -32 or
                        translatedRect.bottom >= 512):
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

def main():
    import game
    import sprite
    import os
    import pygame
    import camera

    class MyGame(game.Game):
        def __init__(self):
            game.Game.__init__(self)
            player = sprite.Hero()
            player.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (0,0), (96,128))
            player.speed_is(2)
            #player.walking_boundary_is(640, 480)

            npc = sprite.Npc()
            npc.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,128), (96,128))
            npc.speed_is(2)
            npc.walking_boundary_is(640, 480)
            npc.set_walking_mode(2)

            npc1 = sprite.Npc()
            npc1.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,0), (96,128))
            npc1.speed_is(1)
            npc1.walking_boundary_is(640, 480)
            npc1.set_walking_mode(1)

            cam = camera.Camera()
            cam.follow(player)

            self.gameWorld = World()
            self.gameWorld.addEntities(player)
            self.gameWorld.addEntities(npc)
            self.gameWorld.addEntities(npc1)
            self.gameWorld.setCamera(cam)

            self.img_master = pygame.image.load(os.path.join("..\graphics\Parallaxes", "FinalFantasy.jpg")).convert()
            self.bgd_rect = pygame.Rect(0,0,640,480)
            self.background = self.img_master.subsurface((self.bgd_rect))
##            self.background.fill((255,255,255))

            self.img_master2 = pygame.image.load(os.path.join("..\graphics\Parallaxes", "FinalFantasy.jpg")).convert()
            self.bgd_rect2 = pygame.Rect(0,0,640,480)
            self.background2 = self.img_master2.subsurface((self.bgd_rect))

            self.img_master3 = pygame.image.load(os.path.join("..\graphics\Parallaxes", "FinalFantasy.jpg")).convert()
            self.bgd_rect3 = pygame.Rect(0,0,640,480)
            self.background3 = self.img_master3.subsurface((self.bgd_rect))


        def update(self):
            tmp_rect = self.bgd_rect.move(-self.gameWorld.camera.offset[0], -self.gameWorld.camera.offset[1])
    #        print(cam.offset, bgd_rect.move(-cam.offset[0], -cam.offset[1]))
            if tmp_rect.left < 0:
                tmp_rect.left = 0
    #        elif tmp_rect.right > 1024:
    #            tmp_rect.right = 1024
            if tmp_rect.top < 0:
                tmp_rect.top = 0
    #        elif tmp_rect.bottom > 945:
    #            tmp_rect.bottom = 945
##            print(tmp_rect, player.rect)

            tmp_rect2 = self.bgd_rect2.move(-self.gameWorld.camera.offset[0], -self.gameWorld.camera.offset[1])
    #        print(cam.offset, bgd_rect.move(-cam.offset[0], -cam.offset[1]))
            if tmp_rect2.left < 0:
                tmp_rect2.left = 0
    #        elif tmp_rect.right > 1024:
    #            tmp_rect.right = 1024
            if tmp_rect2.top < 0:
                tmp_rect2.top = 0
    #        elif tmp_rect.bottom > 945:
    #            tmp_rect.bottom = 945

            tmp_rect3 = self.bgd_rect3.move(-self.gameWorld.camera.offset[0], -self.gameWorld.camera.offset[1])
    #        print(cam.offset, bgd_rect.move(-cam.offset[0], -cam.offset[1]))
            if tmp_rect3.left < 0:
                tmp_rect3.left = 0
    #        elif tmp_rect.right > 1024:
    #            tmp_rect.right = 1024
            if tmp_rect3.top < 0:
                tmp_rect3.top = 0
    #        elif tmp_rect.bottom > 945:
    #            tmp_rect.bottom = 945

            self.background = self.img_master.subsurface((tmp_rect))
            self.background2 = self.img_master2.subsurface((tmp_rect2))
            self.background3 = self.img_master3.subsurface((tmp_rect3))
            self.gameWorld.update()
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.background2,(0,0))
            self.screen.blit(self.background3,(0,0))
            self.gameWorld.render(self.screen)

    zelda = MyGame()
    zelda.start()

if __name__ == '__main__':
    main()
