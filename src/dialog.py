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
    BOTTOM = (320, 390)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bgk = pygame.image.load(os.path.join("..", "graphics", "System", "paper.jpg")).convert()
        self.image = pygame.Surface((555, 135))
        self.image.blit(self.bgk, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 160)
        self.icon = None
        self._makeArrow()
        #use for advancing text
        self.endPos = 0
        self.startPos = 0
        self.pause = False
        self.messages = ""
        self.personImage = None

        self.margine = (10, 10)
##        self.font = pygame.font.SysFont("None", 30)
        self.font = pygame.font.Font(os.path.join("..", "font","default.ttf"), 18)

##        self.messages = """This is simple message dialog box that can be tested
##                           any time we want so we change easily. And now what can
##                           I write to make this dialog box going on and on so long
##                           that we have test because in reality, we will use a very long
##                           message instead of this. This is simple message dialog box that can be tested
##                           any time we want so we change easily. And now what can
##                           I write to make this dialog box going on and on so long
##                           that we have test because in reality, we will use a very long
##                           message instead of this."""

        self.pages = len(self.messages)
        self.page = 0

        self.visable = False

        self._setUpSound()

    def _setUpSound(self):
        self.soundBox = Jukebox()
        self.soundStart = False

    def draw(self, surface, location = BOTTOM):

        def drawDialog():
            surface.blit(self.image, self.rect)
            surface.blit(self.icon, ((surface.get_width() - self.icon.get_width()) / 2, 20))

        if not self.visable:
            return

        if self.pause:
            drawDialog()
            self.soundStart = False
            return

        self.rect.center = location
        xpos = self.margine[0]
        ypos = self.margine[1]

        self.currMessage = self.messages[self.page]
        message = self.currMessage[self.startPos:self.endPos]

        for word in message.split():
            ren = self.font.render(word + u" " , True, (255,255,255))
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
                self.pause = True

        if self.endPos == len(self.currMessage):
            self.image.blit(self.arrow,(300,125))
            self.pause = True

        drawDialog()

    def _makeArrow(self):
        img = pygame.Surface((20, 15))
        img.fill((226, 59, 252))
        img.set_colorkey((226, 59, 252), pygame.RLEACCEL)
        pygame.draw.polygon(img, (0,100,30), ((0, 0), (6, 6), (10, 0)))
        self.arrow = img

    def resetBox(self):
        """reseting the dialog box so it erase all the text rendered on it
        """
        self.image.blit(self.bgk,(0,0))   

    def update(self):
        if not self.visable:
            return

        self.keyHandler()
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

    def keyHandler(self):
        """
            This will handle the keyboard input
        """

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:

            if self.endPos == len(self.currMessage):
                self.page += 1
                self.startPos = 0
                self.endPos = 0
                if self.page >= self.pages:
                    self.visable = False
                
                return

            self.resetBox()
            self.pause = False


    def setMessage(self, content):
        self.messages = content["msgList"]

        if "image" in content:
            if content["image"] == None:
                self.personImage = None
            else:
                self.personImage = content["image"]
        
        
        self.pages = len(self.messages)
        self.page = 0
        self.pause = False
        self.soundStart = True
        self.currMessage = self.messages[self.page]
        self.visable = True

        #setting icon for now it is just the same icon all the time
        image = pygame.image.load(os.path.join("..", "graphics", "Faces", self.personImage)).convert_alpha()

        self.icon = pygame.Surface((96,96)).convert()
        self.icon.fill((100,80,150))
        self.icon.blit(image, (0,0))
        self.resetBox()

