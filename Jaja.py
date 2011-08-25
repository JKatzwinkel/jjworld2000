import pygame
import random
import math
import operator

import Pathfinder
import Images




class Jaja(pygame.sprite.Sprite):
	image=None
	
	ACT_SLEEP=0
	ACT_STAND=1
	ACT_WALK=2
	
	
	
	def __init__(self, location, mp):
		pygame.sprite.Sprite.__init__(self)
		
		if not(Jaja.image):
			Jaja.image=pygame.image.load("data/jaja00.png").convert_alpha()
			
		self.image=Jaja.image
		
		self.map=mp
		
		self.location=location
		self.currentmapnode=self.map.getNode((int(round(self.location[0])),int(round(self.location[1]))))
		
		self.areaOnScreen=None
		
		self.pathfinder=Pathfinder.Pathfinder(self.map)
		self.path=[]
		
		
		self.energy=0
		self.fed=0
		self.action=Jaja.ACT_SLEEP
		

		
	
	# compute the position relative to the screen's position
	def locationOnScreen(self):
	
		x,y=self.location
		sx,sy=self.map.gfx.topleft
		x=x*20-sx
		y=y*20-sy+int(self.currentmapnode.water>0)*2
		return (int(x),int(y))
		
	
		
		
	
	# method to be called in every loop
	# calls the move-method which updates the position of the character
	def update(self):

		if self.fed>0:
			self.fed-=.1


		# sleep		
		if self.action is Jaja.ACT_SLEEP:
			self.energy+=.001+random.random()*.001
			if self.energy>1:
				if random.random()<.05:
					self.action=Jaja.ACT_STAND
			
			
		# stand
		if self.action is Jaja.ACT_STAND:
		
			if len(self.path)==0:
				if self.pathfinder.getpath():
					self.path=self.pathfinder.getpath()
					self.action=Jaja.ACT_WALK
				else:
					# tired ?
					if self.energy<.4:
						if self.currentmapnode.vegetation>1:
							self.action=Jaja.ACT_SLEEP
						else:
							# look for place to sleep
							# TODO!!!!
							x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
							kn=self.map.getNode((x,y))
							if not( kn in self.map.waternodes or kn.vegetation<2):
								self.pathfinder.find(self.getlocation(), (x, y))
							
					else:	
						if random.random()<.01:
							x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
							while self.map.getNode((x,y)) in self.map.waternodes:
								x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
							self.pathfinder.find(self.getlocation(), (x, y))

			# conduct limited steps of a*-algorithm path search
			if self.pathfinder.searching:
				for i in range(0,3):
					self.pathfinder.search()



		# set the background range which has been occupied by the character as to be redrawn
		if self.areaOnScreen:
			self.map.gfx.setDirty(self.areaOnScreen)


		# walk
		if self.action is Jaja.ACT_WALK:
			self.move()
		
		
		
		
	
	# take care of movement
	def move(self):
		x,y=self.location
		nx,ny=self.currentmapnode.location
		
		# to be opt
		if x>nx+.5 or x<nx-.5 or y>ny+.5 or y<ny-.5:
			self.currentmapnode=self.map.getNode(self.getlocation())
			self.map.shrink(self.currentmapnode)
		
		
		if len(self.path)>0:
			#print len(self.path)
			
			dest=self.path[len(self.path)-1]
			dx,dy=dest.location
			
			mx=dx-x
			my=dy-y
			rad=math.hypot(mx,my)			
			
			
			if rad>.2:
				cost=self.currentmapnode.cost()
				speed=.1/cost * self.energy
				mx/=rad
				my/=rad
				x+=mx*speed
				y+=my*speed
				self.location=(x,y)
				if self.energy>.2:
					self.energy-=.001/cost
			else:
				self.path.pop()
		else:
			self.action=Jaja.ACT_STAND
				
				
			
	# draw the punk to the given surface
	def draw(self, surface):

		location=map(operator.mul, self.location, (20,20))
		self.areaOnScreen=pygame.Rect(location, (20,22))
		
		los=self.locationOnScreen()

		if not(self.currentmapnode.water>0):
			surface.blit(Images.getJajaImage(self), los)
		else:
			x,y=los
			surface.blit(Images.getJajaImage(self), (x,y), (0,0,20,12))
		
		if self.pathfinder.searching:
			pos=map(operator.add,los,(-9,-7))
			surface.blit(Images.getIconImage(Images.ICON_BUBBLE), pos)

			self.areaOnScreen=pygame.Rect(map(operator.add, location, (-9,-7)), (29,27))
			
		pygame.draw.line(surface, (200,0,0), los, map(operator.add, los, (int(self.energy*5),0) ))


	# determine the map square on which the character is currently standing on 			
	def getlocation(self):
		return (int(round(self.location[0])), int(round(self.location[1])))
		

