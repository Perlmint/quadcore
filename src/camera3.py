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
from map import Map
from random import randint

class Camera(object):

    def __init__(self):
##        #create tile image list so a big image will be splited into small square
##        #and put into a list according to its possition in the big image
##        #01234      = [0, 1, 2, 3, 4,
##        #56789        5, 6, 7, 8, 9]
##        #whil 0 through 9 is linked as whole piece of image
##        self.bgImage = pygame.image.load('../graphics/Parallaxes/bg1.jpg').convert()
##        self.tile_image = []
##        for tile_y in range(self.bgImage.get_height()/32):
##            for tile_x in range(self.bgImage.get_width()/32):
##                self.tile_image.append((self.bgImage.subsurface((tile_x*32, tile_y*32), (32,32))).convert())
##        self.map = Map()
##        self.map.load(os.path.join("..\map", "test.tmx"))

##        #create a random map
##        #tile_map is a list that has the number associated in tile_image above
##        #This tile_map should be created with map editor
##        self.tile_map = []
##        self.tile_map2 = []
##        self.tile_map3 = []
##        num_tile_x = 100
##        num_tile_y = 100
##        for tile_y in range(num_tile_y):
##            self.tile_map.append([])
##            for tile_x in range(num_tile_x):
##                self.tile_map[tile_y].append(randint(0, len(self.tile_image)-1))
##
##        for tile_y in range(num_tile_y):
##            self.tile_map2.append([])
##            for tile_x in range(num_tile_x):
##                self.tile_map2[tile_y].append(randint(0, len(self.tile_image)-1))
##
##        for tile_y in range(num_tile_y):
##            self.tile_map3.append([])
##            for tile_x in range(num_tile_x):
##                self.tile_map3[tile_y].append(randint(0, len(self.tile_image)-1))

##        self.map_size_x = num_tile_x * 32
##        self.map_size_y = num_tile_y * 32
##        self.map_size_x = self.map.tmxMap.width * 32
##        self.map_size_y = self.map.tmxMap.height * 32

##        #tile_pos_list is the list of position for the tile_map list
##        self.tile_pos_list = self.map.posList
##        for tile_y in range(num_tile_y):
##            self.tile_pos_list.append([])
##            for tile_x in range(num_tile_x):
##                self.tile_pos_list[tile_y].append((tile_x*32,tile_y*32))

        #cordX and cordY are used to translate object to be blited in camera
        self.cordX = 0
        self.cordY = 0
        #windowX and windowY are used to determine when to move the camera's cordinate
        self.windowX = 80
        self.windowY = 80
        #dx and dy is the movement of camera
        self.dx = 0
        self.dy = 0

        self.world = None

        self.follow = None      #the target that camera will move with
##        self.rect = pygame.Rect(0,0,640, 480)
##        self.vpX = 0
##        self.vpY = 0
##        self.viewport = pygame.Surface((640, 480))

##        self.dx = 0
##        self.dy = 0

##
##        self.x_windows = 80
##        self.y_windows = 80
##        self.image = pygame.Surface((640-self.x_windows, 480-self.y_windows)).convert()
##        self.image.fill((100,100,100))
##        self.image.set_alpha(100)
##        self.rect = self.image.get_rect()
    def addWorld(self, world):
        self.world = world
        self.map_size_x = world.map.tmxMap.width * 32
        self.map_size_y = world.map.tmxMap.height * 32
        self.tile_pos_list = world.map.posList

    def translate(self, rect):
        return rect.move(-self.cordX, -self.cordY)

    def update(self):
        #set dx and dy to its follow's speed so it move the same speed
        self.dx = self.follow.speed
        self.dy = self.follow.speed
##        self.follow.update()

##        self.rect.centerx = self.follow.rect.centerx - self.vpX
##        self.rect.centery = self.follow.rect.centery - self.vpY


#        self.dx = 0
#        self.dy = 0

        # check if we need to move the camera
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
##        if self.rect.left <= 0:
##            self.rect.centerx = self.follow.rect.centerx - self.vpX
##            self.dx = -3
##
###            print(self.dx)
##        elif self.rect.right >= 640:
##            self.rect.centerx = self.follow.rect.centerx - self.vpX
##            self.dx = 3
##        if self.rect.top <= 0:
##            self.rect.centery = 240
##            self.dy = -3
##        elif self.rect.bottom >= 480:
##            self.rect.centery = 240
##            self.dy = 3

##        top = self.cordY/32
##        bottom = (480+self.cordY)/32 + 1
##        left = self.cordX/32
##        right = (640+self.cordX)/32 + 1
##
##        if top < 0: top =0
##        if left < 0: left = 0
##
##        for tile_y in self.tile_pos_list[top:bottom]:
##            for tile_x in tile_y[left:right]:
##                self.viewport.blit(self.tile_image[self.tile_map[tile_x[1]/32][tile_x[0]/32]],
##                                    (tile_x[0]-self.cordX, tile_x[1]-self.cordY))


##        self.viewPort.blit(self.follow.image, (self.follow.rect.centerx - self.cordX, self.follow.rect.centery - self.vpY))
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
##                surface.blit(self.map.getImage(tile_x[0]/32, tile_x[1]/32, layer),
##                            (tile_x[0]-self.cordX, tile_x[1]-self.cordY))
##                surface.blit(self.tile_image[self.tile_map[tile_x[1]/32][tile_x[0]/32]],
##                                    (tile_x[0]-self.cordX, tile_x[1]-self.cordY))

##                surface.blit(self.tile_image[self.tile_map2[tile_x[1]/32][tile_x[0]/32]],
##                                    (tile_x[0]-self.cordX, tile_x[1]-self.cordY))
##
##                surface.blit(self.tile_image[self.tile_map3[tile_x[1]/32][tile_x[0]/32]],
##                                    (tile_x[0]-self.cordX, tile_x[1]-self.cordY))
    def render(self, surface, worldMap, layer):
        top = self.cordY/32
        bottom = (480+self.cordY)/32 + 1
        left = self.cordX/32
        right = (640+self.cordX)/32 + 1

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

def main():
    import os
    import sprite
    import world
    import npc

    pygame.init()

#    try:
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Testing")

    ##        background = pygame.Surface((640, 480))
    ##        background.fill((255,255,255))
##    img_master = pygame.image.load(os.path.join("..", "graphics", "Parallaxes", "FinalFantasy.jpg")).convert()
##    bgd_rect = pygame.Rect(0,0,640,480)
##    background = img_master.subsurface((bgd_rect))

    clock = pygame.time.Clock()
    keepGoing = True

    gameWorld = world.World()
    worldMap = Map()
    worldMap.load(os.path.join("..", "map", "test.tmx"))
    gameWorld.addMap(worldMap)

    player = sprite.Hero()
    player.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor1.png"), (32,32), (0,0), (96,128))
    player.speed_is(3)
    player.walking_boundary_is(worldMap.size[0], worldMap.size[1])
    player.set_pos(200, 200)
##    player.walking_boundary_is(1024, 945)

##    npc = sprite.Npc()
##    npc.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,128), (96,128))
##    npc.speed_is(2)
##    npc.walking_boundary_is(640, 480)
##    npc.set_walking_mode(2)
##
##    npc1 = sprite.Npc()
##    npc1.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,0), (96,128))
##    npc1.speed_is(1)
##    npc1.walking_boundary_is(640, 480)
##    npc1.set_walking_mode(1)

    for num in xrange(10):
        tempNpc = sprite.Npc()
        tempNpc.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor1.png"), (32,32), (96,0), (96,128))
        tempNpc.speed_is(1)
        tempNpc.set_walking_mode(1)
        gameWorld.addEntities(tempNpc)

    for num in xrange(10):
        tempNpc = sprite.Npc()
        tempNpc.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor1.png"), (32,32), (288,128), (96,128))
        tempNpc.speed_is(1)
        tempNpc.set_walking_mode(1)
        tempNpc.set_pos(100,800)
        gameWorld.addEntities(tempNpc)

    for num in xrange(10):
        tempNpc = sprite.Npc()
        tempNpc.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor3.png"), (32,32), (96,0), (96,128))
        tempNpc.speed_is(1)
        tempNpc.set_walking_mode(1)
        tempNpc.set_pos(900,100)
        gameWorld.addEntities(tempNpc)

    for num in xrange(10):
        tempNpc = sprite.Npc()
        tempNpc.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor2.png"), (32,32), (96,0), (96,128))
        tempNpc.speed_is(3)
        tempNpc.set_walking_mode(1)
        tempNpc.set_pos(900,800)
        gameWorld.addEntities(tempNpc)

    myRpgNpc = npc.MyRpg()
    myRpgNpc.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor2.png"), (32,32), (96,0), (96,128))
    myRpgNpc.set_pos(700, 400)
    gameWorld.addEntities(myRpgNpc)

    myRpgNpc = npc.Zelda()
    myRpgNpc.set_pos(800,600)
    gameWorld.addEntities(myRpgNpc)

    gameWorld.addEntities(player)
##    gameWorld.addEntities(npc)
##    gameWorld.addEntities(npc1)

##    player.add_unwalkable_sprite(npc)
##    player.add_unwalkable_sprite(npc1)
##
##    npc.add_unwalkable_sprite(player)
##    npc.add_unwalkable_sprite(npc1)
##
##    npc1.add_unwalkable_sprite(player)
##    npc1.add_unwalkable_sprite(npc)
##
##    npc_group = group.Group()
##    player_group = group.Group()

##    npc_group.add(npc)
##    npc_group.add(npc1)

    cam = Camera()
    cam.set_follow(player)
    gameWorld.setCamera(cam)

##    player_group.add(player)

    while keepGoing:
        clock.tick(32)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                keepGoing = False



##        tmp_rect = bgd_rect.move(-cam.offset[0], -cam.offset[1])
###        print(cam.offset, bgd_rect.move(-cam.offset[0], -cam.offset[1]))
##        if tmp_rect.left < 0:
##            tmp_rect.left = 0
###        elif tmp_rect.right > 1024:
###            tmp_rect.right = 1024
##        if tmp_rect.top < 0:
##            tmp_rect.top = 0
###        elif tmp_rect.bottom > 945:
###            tmp_rect.bottom = 945
##        print(tmp_rect, player.rect)
##        background = img_master.subsurface((tmp_rect))
##
##        player_group.update()
##        npc_group.update()
##        cam.update()
        gameWorld.update()
##        screen.blit(cam.viewPort,(0,0))
        gameWorld.render(screen)


##        screen.blit(background, (0,0))
##        player_group.draw(screen, cam)
##        npc_group.draw(screen, cam)

        pygame.display.flip()
    ##            raise Error

#    except: pass

    pygame.quit()

if __name__ == "__main__":
    main()
