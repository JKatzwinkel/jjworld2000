import pygame
import random
import math
import operator

import Pathfinder
import Images
import BFSHandler




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
		
		self.bfs=BFSHandler.BFSHandler()
		
		
		self.energy=.4
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
			self.energy+=.001+self.currentmapnode.vegetation*.001
			if self.energy>1:
				if random.random()<.05:
					self.action=Jaja.ACT_STAND
			
			
		# stand
		if self.action is Jaja.ACT_STAND:
		
			if self.pathfinder.getpath():
			
				self.path=self.pathfinder.path
				self.action=Jaja.ACT_WALK
				
			else:
			
				if not(self.pathfinder.searching):
				
					found=self.bfs.getFound()
					if found:
						
						self.pathfinder.find(self.currentmapnode.location, found.location)
						
					else:
					
						if not(self.bfs.searching):
							
							if self.energy<.4:
								
								if self.currentmapnode.fertility()>6:
									
									self.action=Jaja.ACT_SLEEP
									
								else:
								
									self.bfs.find(self.currentmapnode, 0)
							
							else:
								# find path to random point on the map
								# TODO find destinations which are actually making sense
								if random.random()<.01:
									x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
									node=self.map.getNode((x,y))
									while node in self.map.waternodes or node.vegetation>1:
										x,y=(random.randrange(0,self.map.width),random.randrange(0,self.map.height))
										node=self.map.getNode((x,y))

									self.pathfinder.find(self.getlocation(), (x, y))
									
						else:
							# abort the bfs somehow when reaching a certain depth and lookup in the known-resources list which is TODO
							if self.bfs.depth>20:
								
								print "sleep where I stand"
								self.action=Jaja.ACT_SLEEP
								self.bfs.stop()

			# conduct limited steps of a*-algorithm path search
			if self.pathfinder.searching:
				self.pathfinder.search()
			elif self.bfs.searching:
			# conduct steps in bfs algorithm if no a* running
				self.bfs.search()



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
					self.energy-=.001*(1+cost/20)
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
		
