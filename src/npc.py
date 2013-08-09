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
# Name:        npc.py
# Purpose:     For creating npc with custom respond
#
# Author:      MuyChiv Taing
#
# Created:     09/03/2012
# Copyright:   Copyright MuyChiv Taing 2012
# Licence:     (C) Muychiv Taing
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sprite
import os
import sys

class MyRpg(sprite.Npc):
    def __init__(self):
        super(MyRpg, self).__init__()
        self.set_walking_mode(0)
        self.set_pos(700,500)
        self.start = False


    def action(self):
        if self.start and not self.world.dialog.visable:
            oldDir = os.getcwd()
            gameDir = "../mini game/jpulec-My-RPG"
            os.chdir(gameDir)
            sys.path.insert(0, os.getcwd())
            import Game
            try:
                Game.GameLoop().mainloop()
            except:
                pass
            os.chdir(oldDir)

            self.world.dialog.setMessage({"msgList" : ["Thank you!"]})
            self.kill()
            self.start = False

        if self.world and not self.world.dialog.visable:
            self.world.dialog.setMessage({"msgList" : ["This is a mini game. You will be back when you exit the game.",
                                         "You can play only one time. Please enjoy! Talk to me again when you are ready."]})
            self.start = True

class Zelda(sprite.Npc):
    def __init__(self):
        super(Zelda, self).__init__()
        self.set_walking_mode(0)
        self.set_pos(800,600)
        self.load_sprite_sheet(os.path.join("..", "graphics", "Characters", "Actor3.png"), (32,32), (96,0), (96,128))
        self.start = False


    def action(self):
        if self.start and not self.world.dialog.visable:
            oldDir = os.getcwd()
            gameDir = "../mini game/Zelda-love-Candy-0.3"
            os.chdir(gameDir)
            sys.path.insert(0, os.getcwd())
            sys.path.insert(1, "../mini game/Zelda-love-Candy-0.3/lib")
            sys.path.insert(2, "../mini game/Zelda-love-Candy-0.3/data")
            import game
            try:
                game.main()
            except:
                pass
            os.chdir(oldDir)

            self.world.dialog.setMessage({"msgList" : ["I told you that it is still nnot now working! Thank you!"]})
            self.kill()
            self.start = False

        if self.world and not self.world.dialog.visable:
            self.world.dialog.setMessage({"msgList" : ["This mini game is not working properly now.",
                                         "You can go to the mini game folder and run the game by itself"]})
        self.start = True


if __name__ == '__main__':
    npc = MyRpg()
