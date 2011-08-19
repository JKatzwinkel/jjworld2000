import pygame
from pygame.locals import *
from pygame.time import Clock
import math

import Map
import Sprites
import GfxHandler

class Jajaworld:

	def init(self, w, h):
	
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)

		self.map=Map.Map(w,h)
		
		self.topleft=(0,0)
		

	def mainLoop(self):
	
		jaja=pygame.sprite.Sprite()
		jaja.image = pygame.image.load("data/jaja.png").convert()
		jy=-30
		jx=0

#		background=pygame.Surface(self.screen.get_size())
#		background.fill((255,255,255))
		
		
		gfx=GfxHandler.GfxHandler(self.map, self.screen)
		
		clock = pygame.time.Clock()
		
#		for n in self.map.nodes:
#			x,y=n.location

		
#		gfx.drawMap(background)
		
#		self.screen.blit(background, (0,0))
#		pygame.display.flip()

		mx=0
		my=0
		
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
#				elif event.type == KEYPRESSED:
			pressed=pygame.key.get_pressed()
			if pressed[K_RIGHT]:
				mx+=5
			if pressed[K_DOWN]:
				my+=5
			if pressed[K_LEFT]:
				mx-=5
			if pressed[K_UP]:
				my-=5
						
				
						
			self.map.grow(10)
			
			#if (mx != 0 or my != 0):
			#	gfx.moveRange((mx,my))
			#	if mx!=0:mx-=mx/abs(mx)
			#	if my!=0:my-=my/abs(my)
				
			x,y=self.topleft
			if not(x+mx<0 or x+mx>self.map.width*20-self.screen.get_size()[0]): x+=mx
			if not(y+my<0 or y+my>self.map.height*20-self.screen.get_size()[1]): y+=my
			self.topleft=(x,y)
			mx=0
			my=0
			
			gfx.update(self.topleft)
			
#			self.screen.blit(jaja.image, (jx,jy))
#			jy+=1
#			jx=int(math.cos(jy/10.0)*30)
			
			pygame.display.flip()
			
			clock.tick(20)


def main():
	w=Jajaworld()
	w.init(100,100)
	w.mainLoop()
	
if __name__ == '__main__': main()
