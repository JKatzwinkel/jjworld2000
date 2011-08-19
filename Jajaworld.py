import pygame
from pygame.locals import *
from pygame.time import Clock
import math

import Map
import GfxHandler

class Jajaworld:

	def init(self, w, h):
	
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)

		self.map=Map.Map(w,h)
		
		self.topleft=(0,0)
		

	def mainLoop(self):

		
		
		gfx=GfxHandler.GfxHandler(self.map, self.screen)
		
		clock = pygame.time.Clock()
		


		mx=0
		my=0
		
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
#				elif event.type == KEYPRESSED:
			pressed=pygame.key.get_pressed()
			if pressed[K_RIGHT]:
				mx+=6
			if pressed[K_DOWN]:
				my+=6
			if pressed[K_LEFT]:
				mx-=6
			if pressed[K_UP]:
				my-=6
						
				
						
			self.map.grow(2)
			self.map.water_float(30)

			#scrolling
			x,y=self.topleft
			if not(x+mx<0 or x+mx>self.map.width*20-self.screen.get_size()[0]): x+=mx
			if not(y+my<0 or y+my>self.map.height*20-self.screen.get_size()[1]): y+=my
			self.topleft=(x,y)
			mx=abs(mx)/2*(int(mx>=0)*2-1)
			my=abs(my)/2*(int(my>=0)*2-1)
			
			gfx.update(self.topleft)
			
			
			pygame.display.flip()
			
			clock.tick(20)


def main():
	w=Jajaworld()
	w.init(100,100)
	w.mainLoop()
	
if __name__ == '__main__': main()
