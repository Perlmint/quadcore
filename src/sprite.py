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
import random, time
import copy
import script
import runner
import heroine
import inputBox
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
        self.walking_mode = 0

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
        #same as above, but check again world's entities
        if self.world:
            self.collidedEntitiesIndex = self.rect.collidelistall([entity for entity in self.world.entities if entity.__class__.__name__ != "Event"])

            #listOfCollideEntites will have at least one entity which this entity
            #don't want to copy the world.entities list as above
            if len(self.collidedEntitiesIndex) > 1:
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

class Hero(BaseSprite):
    def __init__(self):
        BaseSprite.__init__(self)
        self.actionCollideRect = pygame.Rect(self.image.get_rect().inflate(20,20))
        self.category = "player"
        self.lastPressedTime = []

        for i in range(len(pygame.key.get_pressed())):
            self.lastPressedTime.append(0)

        self.action = None
        self.action_object = None

    def update(self):
        BaseSprite.update(self)
        self.actionCollideRect.center = self.rect.center


    def check_event(self):
        keys_pressed_is = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks()

        if self.world.dialog.visable == False:
            if keys_pressed_is[pygame.K_RIGHT]:
                self.move("right")
            elif keys_pressed_is[pygame.K_LEFT]:
                self.move("left")
            if keys_pressed_is[pygame.K_UP]:
                self.move("up")
            elif keys_pressed_is[pygame.K_DOWN]:
                self.move("down")
        
        if keys_pressed_is[pygame.K_SPACE]:
            if currentTime - self.lastPressedTime[pygame.K_SPACE] > 200:

                if self.action == None:
                    if self.world.dialog.pause == True:
                        collideEntityIndex = self.actionCollideRect.collidelistall(self.world.entities)

                        if len(collideEntityIndex) > 1:
                            for index in collideEntityIndex:
                                if not index == self.world.entities.index(self):
                                    self.action_object = self.world.entities[index]
                                    self.action = self.action_object.action()
                                    break

                elif self.world.dialog.choices == None:
                    if not self.action():
                        self.lastPressedTime[pygame.K_SPACE] = self.lastPressedTime[pygame.K_SPACE] + 1000
                        self.action = None

        if(self.world.dialog.choices != None):
            for i in range(pygame.K_1, pygame.K_9 + 1):
                if(keys_pressed_is[i]):
                    number = i - pygame.K_1

                    if number >= len(self.world.dialog.choices['choices']):
                        break
                    
                    if currentTime - self.lastPressedTime[i] > 200:
                        if number >= len(self.world.dialog.choices['choices']):
                            break

                        if self.world.dialog.item_selection:
                            sel = self.world.dialog.choices['choices'][number]
                            scr = sel.script
                            
                            self.world.dialog.choiceSelected()
                                
                            if hasattr(scr, '__call__'):
                                val = inputBox.ask(self.world.screen, u"얼마를 줄까?")
                                
                                self.action = self.action_object.action(scr(int(val)))
                                
                            else:
                                del self.world.loveee.player.items[number]
                                
                                if scr != None:
                                    self.action = self.action_object.action(scr)
                                
                            self.world.dialog.item_selection = False
                            
                        self.world.dialog.item_selection = False
                    else:
                        scr = self.world.dialog.choices['choices'][number].script
                        if scr != None:
                            self.action = self.action_object.action(scr)
                    
        for i in range(len(keys_pressed_is)):
            if keys_pressed_is[i]:
                self.lastPressedTime[i] = currentTime

class Npc(BaseSprite):
    """

    """

    def __init__(self):
        BaseSprite.__init__(self)
        self.category = "npc"
        self.walking_mode = 1

        self.direction_list = ["left", "up", "right", "down"]
        self.current_direction = "up"

    def action(self):
        pass

    def set_walking_mode(self, mode):
        """
            mode = 0, 1, or 2

            0 is standstill, 1 is always walking, 2 is walking stop.
        """
        self.walking_mode = mode

    def other_update(self):
        pass
 
    def direction_handling(self):
        pass
