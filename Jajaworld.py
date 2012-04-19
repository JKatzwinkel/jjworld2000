import pygame
from pygame.locals import *
from pygame.time import Clock
import math
import random
import operator
import os

import Map
import GfxHandler
import Jaja
import resources.Resource
import Images

class Jajaworld:

	def init(self, w, h):
	
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480), HWSURFACE)

		self.map=Map.Map(w,h)
		
		self.topleft=(0,0)
		
		self.gfx=GfxHandler.GfxHandler(self.map, self.screen)
		
	
	# THE MAIN LOOP #
	def mainLoop(self):

		
		
		self.map.initDetails()
		
		clock = pygame.time.Clock()
		
		jajas=[]
		# spawn jajas all in one area:
#		for j in range(0,30):
#			x=random.randrange(self.map.width/2-self.map.width/8,self.map.width/2+self.map.width/8)
#			y=random.randrange(self.map.width/2-self.map.height/8,self.map.height/2+self.map.height/8)
#			jajas.append(Jaja.Jaja((x,y), self.map))
		# spawn jajas at the map's edges
		for j in range(0,40):
			if random.random()<.5:
				x=random.randrange(0,self.map.width)
				y=random.randint(0,1)*(self.map.height-1)
			else:
				x=random.randint(0,1)*(self.map.width-1)
				y=random.randrange(0,self.map.height)
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

		framecnt=0

		# amount of pixels the visible range of the world is moving
		mx=0
		my=0
		# mouse data
		mouse={"position": (0,0)}
		
		
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
				
			if pressed[K_LALT] and pressed[K_s]:
				Images.screenshot(jajas, self.gfx)

			mouse["down"]=False
			mouse["motion"]=False
			
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == MOUSEMOTION:
					mouse["motion"]=True
				elif event.type == MOUSEBUTTONDOWN:
					mouse["down"]=True
					#echo information of map node the mouse is on
					x,y=map(operator.add, pygame.mouse.get_pos(), self.topleft)
					print "mouse pressed @ position ",x/20,y/20
					n= self.map.getNode((x/20,y/20))
					print "coziness at this point: ", n.coziness()
					print "fertility at this point: ", n.fertility()			
					
					if pressed[K_LSHIFT]:
						if not n.resource or n.containsResources(1):
							n.resource=None
							n.spawnResource(1,20)
							

			if mouse["motion"] and pygame.mouse.get_pressed()[0]:
				x,y=pygame.mouse.get_pos()
				ox,oy=mouse["position"]
				mx=ox-x
				my=oy-y

			mouse["position"]=pygame.mouse.get_pos()


#				elif event.type == KEYPRESSED:
						
				
						
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
			
			self.gfx.update(self.topleft)
			
#			self.screen.blit(jaja.image, jaja.locationOnScreen())

			jajas=sorted(jajas, key=lambda jaja:jaja.location[1])
			
			for jaja in jajas:
				jaja.draw(self.screen)
			
			
			pygame.display.flip()
			
			clock.tick(25)
			framecnt+=1
			if framecnt>50:
				self.map.grow(self.map.width*self.map.height/1000)
				framecnt=0






def main():
	w=Jajaworld()
	w.init(100,100)
	w.mainLoop()
	
	
		

	
if __name__ == '__main__': main()


