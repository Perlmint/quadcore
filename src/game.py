#-------------------------------------------------------------------------------
# Name:        game.py
# Purpose:     To simplify game main loop
#
# Author:      MuychivTaing
#
# Created:     16/02/2012
# Copyright:   (c) MuychivTaing 2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from world import World

class Game(object):

    def __init__(self):
        pygame.init()
        self.caption = "Zelda Love Candy"
        self.resolution = (640, 480)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.isGameOver = False

        self.world = World()

    def update(self):
        """overide this to add neccessary update
        """
        self.world.update()
        self.world.render(self.screen)

    def start(self):
        """ start the game
        """
        while not self.isGameOver:
            self.clock.tick(30)
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.isGameOver = True

            self.update()
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.start()
