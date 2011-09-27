import pygame
from pygame.locals import *
from pygame.time import Clock
import math
import random
import operator

import Map
import GfxHandler
import Jaja
import resources.Resource

class Jajaworld:

	def init(self, w, h):
	
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)

		self.map=Map.Map(w,h)
		
		self.topleft=(0,0)
		
	
	# THE MAIN LOOP #
	def mainLoop(self):

		
		gfx=GfxHandler.GfxHandler(self.map, self.screen)
		
		self.map.initDetails()
		
		clock = pygame.time.Clock()
		
		jajas=[]
		for j in range(0,15):
			x=random.randrange(self.map.width/2-self.map.width/8,self.map.width/2+self.map.width/8)
			y=random.randrange(self.map.width/2-self.map.height/8,self.map.height/2+self.map.height/8)
			jajas.append(Jaja.Jaja((x,y), self.map))

		# get some beer			
		for s in range(0,20):
			n=self.map.getNodeByID(random.randrange(0,len(self.map.nodes)))
			if not(n.water>0):
				n.spawnResource(1,20)

		# make some beds
#		for s in range(0,4):
#			n=self.map.getNodeByID(random.randrange(0,len(self.map.nodes)))
#			if not(n.water>0):
#				n.spawnResource(0,1)
		
		# set some bushes
		for b in range(0,100):
			n=self.map.getNodeByID(random.randrange(0,len(self.map.nodes)))
			if not(n.water>0) and n.fertility()>6 and n.fertility()<10:
				n.spawnResource(2,random.randrange(0,10))
				
			
		
#		Jaja.Jaja((10,10),self.map)
#		for x in range(90,11,-1):
#			jaja.path.append(self.map.getNode((x,10)))


		mx=0
		my=0
		
		while 1:

			pressed=pygame.key.get_pressed()

			if pressed[K_RIGHT]:
				mx+=8
			if pressed[K_DOWN]:
				my+=8
			if pressed[K_LEFT]:
				mx-=8
			if pressed[K_UP]:
				my-=8

			for event in pygame.event.get():
				if event.type == QUIT:
					return
				if event.type == MOUSEBUTTONDOWN:
					x,y=map(operator.add, pygame.mouse.get_pos(), self.topleft)
					print "mouse pressed @ position ",x/20,y/20
					n= self.map.getNode((x/20,y/20))
					print "coziness at this point: ", n.coziness()
					print "fertility at this point: ", n.fertility()
					
					if pressed[K_LSHIFT]:
						if not n.resource or n.containsResources(1):
							n.resource=None
							n.spawnResource(1,20)
#				elif event.type == KEYPRESSED:
						
				
						
			self.map.grow(2)
			self.map.water_float(30)

			#scrolling
			x,y=self.topleft
			if not(x+mx<0 or x+mx>self.map.width*20-self.screen.get_size()[0]): x+=mx
			if not(y+my<0 or y+my>self.map.height*20-self.screen.get_size()[1]): y+=my
			self.topleft=(x,y)
			mx=abs(mx)/2*(int(mx>=0)*2-1)
			my=abs(my)/2*(int(my>=0)*2-1)
			

			for jaja in jajas:
				jaja.update()			
			
			gfx.update(self.topleft)
			
#			self.screen.blit(jaja.image, jaja.locationOnScreen())

			jajas=sorted(jajas, key=lambda jaja:jaja.location[1])
			
			for jaja in jajas:
				jaja.draw(self.screen)
			
			
			pygame.display.flip()
			
			clock.tick(25)


def main():
	w=Jajaworld()
	w.init(70,70)
	w.mainLoop()
	
if __name__ == '__main__': main()


