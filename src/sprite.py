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
# Name:        sprite.py
# Purpose:
#
# Author:      MuychivTaing
#
# Created:     19/02/2012
# Copyright:   (c) MuychivTaing 2012
# Licence:     GPL v3
#-------------------------------------------------------------------------------
### file   : sprite.py
### purpose: simply sprite creation

## import installed library
import pygame
import math
from random import randint
## end of import installed library

## import custom library

## end of import custom library


""" attribute:

    restriction:
"""

__author__="Muychiv Taing"
__nickname__="Kenny"
__date__ ="Nov 4, 2010 6:10:58 PM"

class BaseSprite(pygame.sprite.Sprite):
    """ base sprite for all the following class
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()

        self.image_dict = {}

        #animation property
        self.max_frame = 2
        self.frame = 1
        self.stand_frame = 1
        self.current_frame = self.stand_frame
        self.animation_speed = 1
        self.animation_delay = 5
        self.temp = self.animation_speed
        self.direction = "down"
        self.is_walking = False

        #movement property
        self.unwalkable_entity_list = []
        self.unwalkable_layer= None
        self.is_collided = False
        self.speed = 5
        self.movement_x = self.speed          # might be change by camera module
        self.movement_y = self.speed          # might be change by camera module
        self.boundary = None

        #game property
        self.world = None      #can access to the world
        self.collidedObject = []    #collect of all collide object
        self.category = None        #the category of the sprite. hero, npc, ect...

    def kill(self):
        if self.world:
            #this sprite is in a the world
            self.world.killEntity(self)

    def walking_boundary_is(self, dimension_x, dimension_y):
        """ given dimension_x and dimension_y to defince
            how big the sprite can walk. Use this to set world map size.

            For example:

                walking_boundary_is(3000, 2000)
        """
        self.boundary = (dimension_x, dimension_y)

    def action(self):
        """ overide to get a spefic action
        """
        pass

    def speed_is(self, speed):
        """
        """
        self.speed = speed
        self.movement_x = speed
        self.movement_y = speed

    def set_pos(self, x, y):
        """
            specify the center position of the sprite.
        """
        self.rect.center = (x, y)

    def update(self):
        self.check_event()
        self.other_update()
        self._check_collision()
        self._update_animation()

    def load_sprite_sheet(self, spritesheet, charDIM=(32,32), sheetStartPos = (0,0),
                            sheetDIM=(96,128), alpha=False,
                            directionList=["down", "left", "right", "up"]):
        """
        sprite.load_sprite_sheet(self, spritesheet, alpha=False)

        Load a sprite sheet
        """
        tempSheet = pygame.image.load(spritesheet).convert()

        ## spritesheet might have many animaiton, and we want only
        ## a portion of animation
        temp_rect = pygame.Rect(sheetStartPos,(sheetDIM))
        temp_sheet = tempSheet.subsurface(temp_rect)
        temp_row = sheetDIM[1]/charDIM[1]
        temp_collumn = sheetDIM[0]/charDIM[0]

        for row in range(temp_row):
            temp_list = []
            for collumn in range(temp_collumn):
                temp_rect = pygame.Rect((charDIM[0]*collumn,
                                        charDIM[1]*row),
                                       (charDIM))
                temp_image = temp_sheet.subsurface(temp_rect)
                if alpha:
                    temp_image = temp_image.convert_alpha()
                else:
                    trans_color = temp_image.get_at((0,0))
                    temp_image.set_colorkey(trans_color)
                temp_list.append(temp_image)

            self.image_dict[directionList[row]] = temp_list

        self.image = self.image_dict[self.direction][self.stand_frame]

        # should this be function. they are use in __init__ and here
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240
        self.rect.inflate_ip(-5,0)


    def move(self, direction):
        """
        sprite.move(self, direction)

        To make a sprite move

        Give direction as a string: "up", "down", "left", or "right"
        """
        self.is_walking = True
        self.direction = direction
        self._do_animation()
        #self._check_collision()

        if not self.is_collided:
            if self.direction == "up":
                self.rect.centery -= self.movement_y
            elif self.direction == "down":
                self.rect.centery += self.movement_y
            if self.direction == "left":
                self.rect.centerx -= self.movement_x
            elif self.direction == "right":
                self.rect.centerx += self.movement_x
        else:
            self.is_collided = False

    def _check_collision(self):
##        for sprite in self.unwalkable_entity_list:
##            if self.rect.colliderect(sprite.rect):
##                self.is_collided = True
##                if self.direction == "up":
##                    self.rect.centery += self.movement_y
##                elif self.direction == "down":
##                    self.rect.centery -= self.movement_y
##                if self.direction == "left":
##                    self.rect.centerx += self.movement_x
##                elif self.direction == "right":
##                    self.rect.centerx -= self.movement_x

##        if self.rect.collidelistall(self.unwalkable_entity_list):
##            self.is_collided = True
##            if self.direction == "up":
##                self.rect.centery += self.movement_y
##            elif self.direction == "down":
##                self.rect.centery -= self.movement_y
##            if self.direction == "left":
##                self.rect.centerx += self.movement_x
##            elif self.direction == "right":
##                self.rect.centerx -= self.movement_x

        #same as above, but check again world's entities
        if self.world:
##            #save the original entities list
##            currentEntities = []
##            currentEntities = self.world.entities[:]
##            #remove this entity from the world entities
##            currentEntities.remove(self)
            #retrieve all entites that is collided in the world
##            listOfCollideEntities = self.rect.collidelistall(currentEntities)
            self.collidedEntitiesIndex = self.rect.collidelistall(self.world.entities)

            #listOfCollideEntites will have at least one entity which this entity
            #don't want to copy the world.entities list as above
            if len(self.collidedEntitiesIndex) > 1:
##                print(listOfCollideEntities)
                if self in self.collidedEntitiesIndex:
                    print("I am collide with my self")
                #this entity is still collide with other entities
                self.is_collided = True
                if self.direction == "up":
                    self.rect.centery += self.movement_y
                elif self.direction == "down":
                    self.rect.centery -= self.movement_y
                if self.direction == "left":
                    self.rect.centerx += self.movement_x
                elif self.direction == "right":
                    self.rect.centerx -= self.movement_x

            #check collision of teritory
            listOfCollideEntities = self.rect.collidelistall(self.world.map.unwalkable)
            if listOfCollideEntities:
                self.is_collided = True
                if self.direction == "up":
                    self.rect.centery += self.movement_y
                elif self.direction == "down":
                    self.rect.centery -= self.movement_y
                if self.direction == "left":
                    self.rect.centerx += self.movement_x
                elif self.direction == "right":
                    self.rect.centerx -= self.movement_x

        if self.boundary != None:   #boundary is not None
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.boundary[0]:
                self.rect.right = self.boundary[0]
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > self.boundary[1]:
                self.rect.bottom = self.boundary[1]
##
##        #unwalkable layer checking
##        tile_x = int(self.rect.centerx / 32)
##        tile_y = int(self.rect.centery / 32)
##
##        if self.world.map.unwalkableList[tile_y][tile_x]:
##            self.is_collided = True
##            if self.direction == "up":
##                self.rect.centery += self.movement_y
##            elif self.direction == "down":
##                self.rect.centery -= self.movement_y
##            if self.direction == "left":
##                self.rect.centerx += self.movement_y
##            elif self.direction == "right":
##                self.rect.centerx -= self.movement_y


    def add_unwalkable_layer(self, collLayer):
        self.unwalkable_layer = collLayer

    def add_unwalkable_sprite(self, sprite):
        self.unwalkable_entity_list.append(sprite)

    def check_event(self):
        """ This function does nothing. Automatic called in update.
            Overwrite to make a custom check_event.
        """
        pass

    def other_update(self):
        """ This function dose nothing. Automatic called in update.
            Overwrite this function.
        """
        pass

    def _update_animation(self):
        """
            used to update self.image
        """
        if not self.is_walking:
            self.image = self.image_dict[self.direction][self.stand_frame]
        else:
            self.is_walking = False

    def _do_animation(self):
        """ called by move methon.

            used to update frame
        """
        self.temp += self.animation_speed
        if self.temp >= self.animation_delay:
            self.temp = self.animation_speed
            self.image = self.image_dict[self.direction][self.current_frame]

            # not sure but this animation has to do add and substract frame
            # back and forward
            self.current_frame += self.frame
            if self.current_frame < 0:
                self.frame *= -1
                self.current_frame += 1
            elif self.current_frame > self.max_frame:
                self.frame *= -1
                self.current_frame += self.frame

# TODO document this class
class Hero(BaseSprite):
    """

    """
    def __init__(self):
        BaseSprite.__init__(self)
        self.actionCollideRect = pygame.Rect(self.image.get_rect().inflate(20,20))
        self.category = "player"

    def update(self):
        BaseSprite.update(self)
        self.actionCollideRect.center = self.rect.center


    def check_event(self):
        keys_pressed_is = pygame.key.get_pressed()
        if keys_pressed_is[pygame.K_RIGHT]:
            self.move("right")
        elif keys_pressed_is[pygame.K_LEFT]:
            self.move("left")
        if keys_pressed_is[pygame.K_UP]:
            self.move("up")
        elif keys_pressed_is[pygame.K_DOWN]:
            self.move("down")

        if keys_pressed_is[pygame.K_z]:
            collideEntityIndex = self.actionCollideRect.collidelistall(self.world.entities)
            if len(collideEntityIndex) > 1:
##                print(collideEntityIndex)
                for index in collideEntityIndex:
                    if not index == self.world.entities.index(self):
                        self.world.entities[index].action()
                        break
##                    if self.world.entities[index].category == "npc":
##                        self.world.killEntity(self.world.entities[index])
##                        print("one npc has been killed")
##            for entityIndex in self.collidedEntitiesIndex:
##                print(entityIndex)
##                print(self.world.entities[entityIdex])

class Npc(BaseSprite):
    """

    """

    def __init__(self):
        BaseSprite.__init__(self)
        self.category = "npc"
        self.walking_mode = 2
        self.step_count = 0

        self.direction_list = ["down", "up", "left", "right"]
        self.current_direction = "down"
        self.direction_change_frq = 25
        self.current_frequency = 0

    def action(self):
        if self.world and not self.world.dialog.visable:
            self.world.dialog.setMessage({"msgList" : ["Hi I am an Npc who is control by a computer",
                                         "Welcome to the University. How are you doing?"], "image" : "cat.gif"}  )

    def set_walking_mode(self, mode):
        """
            mode = 0, 1, or 2

            0 is standstill, 1 is always walking, 2 is walking stop.
        """
        self.walking_mode = mode

    def other_update(self):

        if self.walking_mode == 0:          #Fixed position, never walk
            pass
        elif self.walking_mode == 1:        #always walk
            self.direction_handling()
            self.move(self.current_direction)
        elif self.walking_mode == 2:        #walk stop walk stop
            if self.step_count == 0:
                self.step_count = randint(-30, 30)

            elif self.step_count < 0:
                self.step_count += 1
            elif self.step_count > 0:
                self.step_count -= 1
                self.direction_handling()
                self.move(self.current_direction)
            #continue here

    def direction_handling(self):
        self.current_frequency += 1
        if self.current_frequency >= self.direction_change_frq:
            self.current_frequency = 0
            temp = randint(0,3)
            self.current_direction = self.direction_list[temp]

if __name__ == "__main__":
    import os
    from world import World
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Testing")

    background = pygame.Surface((640, 480))
    background.fill((255,255,255))

    clock = pygame.time.Clock()
    keepGoing = True
    gameWorld = World()

    player = Hero()
    player.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (0,0), (96,128))
    player.speed_is(3)
    player.set_pos(30,40)
    player.walking_boundary_is(640, 480)


    npc = Npc()
    npc.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,128), (96,128))
    npc.speed_is(2)
    npc.walking_boundary_is(640, 480)
    npc.set_walking_mode(2)

    npc1 = Npc()
    npc1.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,0), (96,128))
    npc1.speed_is(1)
    npc1.walking_boundary_is(640, 480)
    npc1.set_walking_mode(1)

    npc2 = Npc()
    npc2.load_sprite_sheet(os.path.join("..\graphics\Characters", "Actor1.png"), (32,32), (96,0), (96,128))
    npc2.speed_is(1)
    npc2.walking_boundary_is(640, 480)
    npc2.set_walking_mode(1)

    gameWorld.addEntities(player)
    gameWorld.addEntities(npc)
    gameWorld.addEntities(npc1)
    gameWorld.addEntities(npc2)

##    player.add_unwalkable_sprite(npc)
##    player.add_unwalkable_sprite(npc1)
##
##    npc.add_unwalkable_sprite(player)
##    npc.add_unwalkable_sprite(npc1)
##
##    npc1.add_unwalkable_sprite(player)
##    npc1.add_unwalkable_sprite(npc)

    while keepGoing:
        dt = clock.tick()
##        clock.tick(30)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                keepGoing = False

##        player.update()
##        npc.update()
##        npc1.update()
##        npc2.update()
        gameWorld.update()

        screen.blit(background, (0,0))
        screen.blit(player.image, player.rect)
        screen.blit(npc.image, npc.rect)
        screen.blit(npc1.image, npc1.rect)
        screen.blit(npc2.image, npc2.rect)

        pygame.display.flip()
    pygame.quit()