import pygame
import random
import math

import Pathfinder

class Jaja(pygame.sprite.Sprite):
	image=None
	
	
	def __init__(self, location, mp):
		pygame.sprite.Sprite.__init__(self)
		
		if not(Jaja.image):
			Jaja.image=pygame.image.load("data/jaja00.png").convert_alpha()
			
		self.image=Jaja.image
		
		self.map=mp
		
		self.location=location
		self.currentmapnode=self.map.getNode((int(round(self.location[0])),int(round(self.location[1]))))
		
		self.pathfinder=Pathfinder.Pathfinder(self.map)
		self.path=[]
		
		self.firstsearch=True
		
		
	def locationOnScreen(self):
	
		x,y=self.location
		sx,sy=self.map.gfx.topleft
		x=x*20-sx
		y=y*20-sy+int(self.currentmapnode.water>0)*2
		return (int(x),int(y))
		
	
		
	def draw(self, surface):
	
		if not(self.currentmapnode.water>0):
			surface.blit(self.image, self.locationOnScreen())
		else:
			x,y=self.locationOnScreen()
			surface.blit(self.image, (x,y), (0,0,20,12))
		
		
		
	def update(self):
		
		if len(self.path)==0:
			if self.pathfinder.getpath():
				self.path=self.pathfinder.getpath()
			else:
				if random.random()<.01 and self.firstsearch:
					x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
					while self.map.getNode((x,y)) in self.map.waternodes:
						x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
					self.pathfinder.find(self.getlocation(), (x, y))
#					self.firstsearch=False
				
		self.move()
		for i in range(0,5):
			self.pathfinder.search()
		
		
		
	def move(self):
		x,y=self.location
		nx,ny=self.currentmapnode.location
		
		# to be opt
		if x>nx+.5 or x<nx-.5 or y>ny+.5 or y<ny-.5:
			self.currentmapnode=self.map.getNode(self.getlocation())
			self.map.shrink(self.currentmapnode)
		
		self.map.gfx.setDirty((int(x*20),int(y*20)),(20,25))
		
		if len(self.path)>0:
			#print len(self.path)
			
			dest=self.path[len(self.path)-1]
			dx,dy=dest.location
			
			mx=dx-x
			my=dy-y
			rad=math.hypot(mx,my)
			
			
			
			if rad>.1:
				speed=.1/self.currentmapnode.cost()
				mx/=rad
				my/=rad
				x+=mx*speed
				y+=my*speed
				self.location=(x,y)
			else:
				self.path.pop()
			
			
	def getlocation(self):
		return (int(round(self.location[0])), int(round(self.location[1])))
#		else:
#			x,y=self.location
#			self.path.append(self.map.getNode((x-1+random.randint(0,1)*2, y-1+random.randint(0,1)*2)))
