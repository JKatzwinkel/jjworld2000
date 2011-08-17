import pygame
from pygame.locals import *
from time import time

import Map
import Sprites
import GfxHandler

class Jajaworld:

	def init(self, w, h):
	
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)

		self.map=Map.Map(w,h)
		

	def mainLoop(self):
	

#		background=pygame.Surface(self.screen.get_size())
#		background.fill((255,255,255))
		
		
		gfx=GfxHandler.GfxHandler(self.map, self.screen)
		
#		for n in self.map.nodes:
#			x,y=n.location

		
		background = gfx.drawMap()
		
		self.screen.blit(background, (0,0))
		pygame.display.flip()
		
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN:
					pressed=pygame.key.get_pressed()
					if pressed[K_RIGHT]:
						gfx.moveRange((1,0))
						gfx.update()
						pygame.display.flip()
					if pressed[K_DOWN]:
						gfx.moveRange((0,1))
						gfx.update()
						pygame.display.flip()
					if pressed[K_LEFT]:
						gfx.moveRange((-1,0))
						gfx.update()
						pygame.display.flip()
					if pressed[K_UP]:
						gfx.moveRange((0,-1))
						gfx.update()
						pygame.display.flip()
						
			self.map.grow(20)
			gfx.update()
			#pygame.display.flip()


def main():
	w=Jajaworld()
	w.init(100,100)
	w.mainLoop()
	
if __name__ == '__main__': main()
