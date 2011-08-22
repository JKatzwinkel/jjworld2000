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
		

		
	
	# compute the position relative to the screen's position
	def locationOnScreen(self):
	
		x,y=self.location
		sx,sy=self.map.gfx.topleft
		x=x*20-sx
		y=y*20-sy+int(self.currentmapnode.water>0)*2
		return (int(x),int(y))
		
	
		
	# draw the punk to the given surface
	def draw(self, surface):
	
		if not(self.currentmapnode.water>0):
			surface.blit(self.image, self.locationOnScreen())
		else:
			x,y=self.locationOnScreen()
			surface.blit(self.image, (x,y), (0,0,20,12))
		
		
	
	# method to be called in every loop
	# calls the move-method which updates the position of the character
	def update(self):
		
		if len(self.path)==0:
			if self.pathfinder.getpath():
				self.path=self.pathfinder.getpath()
			else:
				if random.random()<.01:
					x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
					while self.map.getNode((x,y)) in self.map.waternodes:
						x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
					self.pathfinder.find(self.getlocation(), (x, y))

				
		self.move()
		
		# conduct limited steps of a*-algorithm path search
		if self.pathfinder.searching:
			for i in range(0,3):
				self.pathfinder.search()
		
		
		
	
	# take care of movement
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
			
			
			if rad>.2:
				speed=.1/self.currentmapnode.cost()
				mx/=rad
				my/=rad
				x+=mx*speed
				y+=my*speed
				self.location=(x,y)
			else:
				self.path.pop()
			

	# determine the map square on which the character is currently standing on 			
	def getlocation(self):
		return (int(round(self.location[0])), int(round(self.location[1])))
		

