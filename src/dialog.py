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
# Name:        dialog.py
# Purpose:     for make conversation with object in the game
#
# Author:      MuychivTaing
#
# Created:     03/03/2012
# Copyright:   (c) MuychivTaing 2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import os
import conch
from conch import Jukebox

class DialogBox(pygame.sprite.Sprite):
    """
        DialogBox class use for dialog or conversation in the game

        Does not work quite well when we skip text or fast forward

        usage:
            messageBox = DialogBox()
            messageBox
    """

    #class constant for setting dialog location
    TOP = (320, 90)
    MIDDLE = (320, 240)
    BOTTOM = (320, 480-52)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.lock = False

        self.bgk = pygame.image.load(os.path.join("..", "graphics", "System", "dialog.png")).convert_alpha()
        self.resetBox()
        self.choiceImage = pygame.Surface((400, 70))
        self.choiceImage.blit(self.bgk, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 480 - 52)
        self.icon = None
        self._makeArrow()
        #use for advancing text
        self.endPos = 0
        self.startPos = 0
        self.pause = True

        self.messages = None
        self.personImage = None
        self.choices = None

        self.margine = (10, 30)
        self.font = pygame.font.Font(os.path.join("..", "font","default.ttf"), 18)

        self.pages = 0
        self.page = 0

        self.visable = False
        
        self.item_selection = False

        self._setUpSound()

    def _setUpSound(self):
        self.soundBox = Jukebox()
        self.soundStart = False

    def draw(self, surface, location = BOTTOM):

        def drawDialog():
            if self.icon != None:
                rect = self.icon.get_rect()
                rect.bottom = self.rect.top + 30
                surface.blit(self.icon, ((surface.get_width() - self.icon.get_width()) / 2, rect.top))
            
            surface.blit(self.image, self.rect)
  

            xpos = self.margine[0]
            ypos = self.margine[1]
            message = self.currMessage[self.startPos:self.endPos]

            for word in message.split():
                ren = self.font.render(word + u" " , True, (33, 33, 33))
                self.image.blit(ren, (xpos, ypos))
                w = ren.get_width()
                xpos += w

                #check for wrapping effect
                if xpos >= (self.image.get_width() - w - 18):
                    xpos = self.margine[0]
                    ypos += ren.get_height() + 4
                elif ypos >= self.image.get_height() - ren.get_height():
                    xpos = self.margine[0]
                    ypos = self.margine[1]
                    self.startPos = self.endPos - 1 #need -1 to have the text start correctly
                    self.image.blit(self.arrow,(540,125))

        if not self.visable:
            return

        if self.pause:
            drawDialog()
            self.soundStart = False
            return

        if self.messages != None:
            self.rect.center = location
            self.currMessage = self.messages[self.page]

            if self.endPos == len(self.currMessage):
                self.image.blit(self.arrow,(300,125))
                self.pause = True

            drawDialog()

        if self.choices != None:
            question = self.choices["question"]
            choices = self.choices["choices"]
       
            xCenter = (surface.get_width() - self.choiceImage.get_width()) / 2
            yMargin = 50

            surface.blit(self.choiceImage, ((surface.get_width() - self.choiceImage.get_width()) / 2, 10))

            ren = self.font.render(question, False, (255,255,255))
            surface.blit(ren, (xCenter + 10, 10))

            i = 0
            for choice in choices:
                i = i + 1
                
                surface.blit(self.choiceImage, (xCenter, i * (self.choiceImage.get_height() + yMargin)))

                ren = self.font.render(str(i) + ". " + choice.name, False, (255,255,255))
                surface.blit(ren, (xCenter + 10,i * (self.choiceImage.get_height() + yMargin) + 10))

    def _makeArrow(self):
        img = pygame.Surface((20, 15))
        img.fill((226, 59, 252))
        img.set_colorkey((226, 59, 252), pygame.RLEACCEL)
        pygame.draw.polygon(img, (0,100,30), ((0, 0), (6, 6), (10, 0)))
        self.arrow = img

    def resetBox(self):
        """reseting the dialog box so it erase all the text rendered on it
        """
        image = pygame.Surface([640,104], pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()
        self.image.blit(self.bgk, (0,0))

    def update(self):
        if not self.visable:
            return

        #check for end of message
        if self.endPos == len(self.currMessage):
            self.soundStart = False
            return

        if self.pause:
            self.soundStart = False

        if not self.soundStart:
            self.soundStart = True


        if not self.pause:
            self.endPos += 1
            if self.endPos >= len(self.currMessage):
                self.endPos = len(self.currMessage)

    def proceedNextMessage(self):
        if self.endPos == len(self.currMessage):
            self.page += 1
            self.startPos = 0
            self.endPos = 0

            if self.page >= self.pages:
                if not self.lock:
                    self.visable = False

            if not self.lock:
                self.resetBox()
                self.pause = False

            return

    def choiceSelected(self):
        if self.choices == None:
            return

        self.choices = None
        self.messages = None
        self.pause = True

    def setMessage(self, content):
        self.messages = content["msgList"]
        self.choices = None

        self.pages = len(self.messages)
        self.page = 0
        self.pause = False
        self.soundStart = True
        self.currMessage = self.messages[self.page]
        self.visable = True
        self.resetBox()

        if "image" in content:
            if content["image"] == None:
                self.personImage = None
                self.icon = pygame.Surface((0,0)).convert()
            else:
                self.personImage = content["image"]

                image = pygame.image.load(os.path.join("..", "graphics", "Faces", self.personImage)).convert_alpha()
                rect = image.get_rect()
                
                self.icon = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32).convert_alpha()
                self.icon.blit(image, (0,0))

    def setChoices(self, choices):
        self.choices = choices
        self.messages = None
        self.pause = False
        self.visable = True
        
        self.page = 0
        self.pause = False
        self.soundStart = True
        self.visable = True

        self.resetBox()
        
        print "setChoice"
