import pygame
from pygame.locals import *

bRunning = True

def gameLoop():
	pass

def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('quadcore')
	while bRunning:
		gameLoop()

if __name__ == "__main__":
	main()
