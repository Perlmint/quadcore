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
# Name:        map.py
# Purpose:     simply tmx loader and map rendering
#
# Author:      MuychivTaing
#
# Created:     20/02/2012
# Copyright:   (c) MuychivTaing 2012
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import tmxloader
import pygame

class Map(object):
    def __init__(self):
        self.tmxMap = None
##        self.world = None
        self.posList = []
        self.unwalkable = []    #a list rect that is collidable
        self.size = None

    def load(self, fileName):
        self.tmxMap = tmxloader.load_pygame(fileName)

        num_tile_y = self.tmxMap.height
        num_tile_x = self.tmxMap.width
        tileWidth = self.tmxMap.tilewidth
        tileHeight = self.tmxMap.tileheight
        self.size = (num_tile_x*tileWidth, num_tile_y*tileHeight)
        #search for collision layer
        collisionLayerIndex = 2
        for layerIndex in xrange(len(self.tmxMap.layers)):
            if self.tmxMap.layers[layerIndex].name == "collision":
##                print("found")
                collisionLayerIndex = layerIndex
                break

        #generate position of every tile image in the world map and collidable rect
        for tile_y in range(num_tile_y):
            self.posList.append([])
            for tile_x in range(num_tile_x):
                self.posList[tile_y].append((tile_x*tileWidth,tile_y*tileHeight))
                #generate collidable rect
                if self.tmxMap.get_tile_image(tile_x, tile_y, collisionLayerIndex):
                    tempRect = pygame.Rect(tile_x*tileWidth, tile_y*tileHeight, self.tmxMap.tilewidth, self.tmxMap.tileheight)
                    oldbottom = tempRect.midbottom
                    tempRect = tempRect.inflate(-10, -10)
                    tempRect.midbottom = oldbottom
                    self.unwalkable.append(tempRect)
##        print(self.unwalkable)

    def getImage(self, x, y, layer):
        """
        return the tile image for this location
        x and y must be integers and are in tile coordinates, not pixel

        return value will be 0 if there is no tile with that location.
        """
        return self.tmxMap.get_tile_image(x, y, layer)

    def getPosition(self, x, y):
        """return the position in pixel (pixelX, pixelY) according to x, y
           x and y must be integers and are in tile coordinates, not pixel
        """
        return self.posList[y][x]

def main():
    pass

if __name__ == '__main__':
    main()