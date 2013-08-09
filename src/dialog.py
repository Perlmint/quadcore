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
        #create a temporery dialog background
##        self.image = pygame.Surface((555, 135))     #height might be chnage to hide one blit at the very bottom
##        self.image.fill((0,0,0))
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

        self.margine = (140, 10)
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

        self.messages = ["This is simple message dialog box that can be tested any time we want so we change easily.",
                         "And now what can I write to make this dialog box going on and on so long that we have test because in reality, we will use a very long message instead of this.",
                         "This example is sample only and now this is the end of our conversation"]
##        self.currMessage = self.messages2[0]
        self.pages = len(self.messages)
        self.page = 0

##        self.setMessage(self.messages2)    #uncommond this to for testing

        self.visable = False

        self._setUpSound()

    def _setUpSound(self):
##        conch.conchinit(44100)
        self.soundBox = Jukebox()
        self.soundBox.LoadSound("Knock3.ogg")
        self.soundStart = False
##        self.soundBox.LoadSong("Knock2.ogg", "message")
##        self.soundBox.PlaySong("message", -1)
##        self.soundBox.SetSoundVolume("Cursor", 10)

    def draw(self, surface, location = BOTTOM):
        if not self.visable:
            return

        if self.pause:
            surface.blit(self.image, self.rect)
            self.soundBox.StopSound("Knock3.ogg")
            self.soundStart = False
            return

        self.rect.center = location
        xpos = self.margine[0]
        ypos = self.margine[1]

##        if self.page >= self.pages:
##            print("self.page - 1")
##            self.page = self.pages - 1

        self.currMessage = self.messages[self.page]
        message = self.currMessage[self.startPos:self.endPos]

        for word in message.split():
            ren = self.font.render(word + " " , False, (255,255,255))
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

##                self.soundBox.StopSound("Knock2.ogg")
##                self.soundBox.StopMusic()
##            self.soundBox.PlaySound("Knock2.ogg")
##            self.soundBox.StopSound("Cursor3.wav")
        if self.endPos == len(self.currMessage):
            self.image.blit(self.arrow,(300,125))
            self.pause = True

        surface.blit(self.image, self.rect)

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
        self.image.blit(self.icon, (20,20))

    def update(self):



        if not self.visable:
            self.soundBox.StopSound("Knock3.ogg")
            return

        self.keyHandler()
        #check for end of message
        if self.endPos == len(self.currMessage):
            self.soundBox.StopSound("Knock3.ogg")
            self.soundStart = False
            return

        if self.pause:
            self.soundBox.StopSound("Knock3.ogg")
            self.soundStart = False

        if not self.soundStart:
            self.soundBox.PlaySound("Knock3.ogg", -1)
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
                    self.soundBox.StopSound("Knock3.ogg")
##                    self.page = self.pages - 1
                return

##            if not self.pause and self.visable and (self.endPos - self.startPos) > 10:
##                #skip 30 character
##                self.endPos += 30

            self.resetBox()
            self.pause = False


    def setMessage(self, msgList, icon = None):
        #ToDo be able the have appropriate icon for the talker
        self.messages = msgList   #" ".join(msgList)
        self.pages = len(self.messages)
        self.page = 0
        self.pause = False
        self.soundBox.PlaySound("Knock3.ogg", -1)
        self.soundStart = True
        self.currMessage = self.messages[self.page]
        self.visable = True

        #setting icon for now it is just the same icon all the time
        self.icon = pygame.Surface((96,96)).convert()
        self.icon.fill((100,80,150))
        image = pygame.image.load(os.path.join("..", "graphics", "Faces", "people1.png")).convert_alpha()
        self.icon.blit(image, (0,0))
        self.resetBox()

if __name__ == '__main__':
    import dialog
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    background = pygame.Surface((640, 480))
    background.fill((255,255,255))

    dialog = DialogBox()

    keepGoing = True
    clock = pygame.time.Clock()

    while keepGoing:
        clock.tick(30)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                keepGoing = False
            elif events.type == pygame.KEYDOWN:
                if not dialog.visable:
                    dialog.setMessage(dialog.messages)
##                    dialog.setMessage(["This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested.",
##                                       "This is simple message dialog box that can be tested."])


        screen.blit(background, (0,0))
        if dialog.visable:
##            print("dialog processing")
            dialog.update()
            dialog.draw(screen)
        pygame.display.flip()

    pygame.quit()
