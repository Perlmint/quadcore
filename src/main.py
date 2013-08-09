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
# Name:        main.py
# Purpose:     The entry file for game
#
# Author:      MuyChiv Taing
#
# Created:     09/03/2012
# Copyright:   Copyright MuyChiv Taing 2012
# Licence:     GPL v3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import game
import camera3
import npc

##class Main(game.Game):
##    def __init__(self):
##        super(Main, self).__init__()
##        npc1 = npc.MyRpg()
##        self.world.addEntities(npc1)
##        camera = camera3.Camera()


if __name__ == '__main__':
##    mainGame = Main()
##    mainGame.start()
    import camera3
    camera3.main()
