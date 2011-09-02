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
		
		self.knownsources=[]
		
		
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
			self.fed-=.001


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
			
				# if not currently conducting an a* search
				if not(self.pathfinder.searching):
				
					found=self.bfs.getFound()
					# is there already a certain node found by the breadth first search?
					if found:
						
						self.pathfinder.find(self.currentmapnode.location, found.location)
						
						# is that result already known?
						if not found in self.knownsources:
							self.knownsources.append(found)
							print "length of known resources list:", len(self.knownsources)
						
					# if there is not yet a result of any breadth first search:					
					else:

						# if not conducting a breadth first search right now:
						if not(self.bfs.searching):
							
							# if tired:
							if self.energy<.4:
								
								if self.currentmapnode.fertility()>6:
									
									self.action=Jaja.ACT_SLEEP
									
								else:
								
									self.bfs.find(self.currentmapnode, 0)
									
							# if not tired:
							else:
								
								# if hungry:
								if self.fed<.5:
								
									#TODO
									if self.currentmapnode.resource and self.currentmapnode.resource.type in (1,):
										self.fed+=1
										
									else:	
										# find beer
										dest = self.getKnownSourceFor((1,))
										
										if not dest:
											self.bfs.find(self.currentmapnode, 1)

									
								# find path to random point on the map
								#
								if random.random()<.01:
									self.goAnyWhere()
						
						
						# if a breadth first search is currently running:
						else:
							# abort the bfs somehow when reaching a certain depth and lookup in the known-resources list which is TODO
							if self.bfs.depth>10:
								
								# if tired
								if self.energy<.5:
								
									print "sleep where I stand"
									self.action=Jaja.ACT_SLEEP
									self.bfs.stop()
									
								# if not tired, but hungry:
								elif self.fed<.5:
								
									dest = self.getKnownSourceFor((1,))
									
									if not dest: 
										# if there a no known beer sources, abort search
										self.bfs.stop()
										self.goAnyWhere()
								
								
								# if nothing has been found as of the depth of 20, stop searching
								if self.bfs.depth>15:
									self.bfs.stop()
									self.goAnyWhere()
								
								

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
				if self.energy>.25:
					self.energy-=.0005*(1+cost/30)
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
		pygame.draw.line(surface, (200,0,0), map(operator.add,los,(0,1)), map(operator.add, los, (int(self.fed*5),0) ))



	# determine the map square on which the character is currently standing on 			
	def getlocation(self):
		return (int(round(self.location[0])), int(round(self.location[1])))
		
		

	# just find a random destination of close distance that is easy to walk and dry
	# start finding a path to there using a*		
	def goAnyWhere(self):
	
		jx,jy=self.currentmapnode.location
		x,y=(random.randrange(jx-6,jx+7),random.randrange(jy-6,jy+7))
		node=self.map.getNode((x,y))
		while not(node) or node in self.map.waternodes or node.vegetation>3:
			x,y=(random.randrange(jx-5,jx+6),random.randrange(jy-5,jy+6	))
			node=self.map.getNode((x,y))

		self.pathfinder.find(self.getlocation(), (x, y))
		
		
		
	# checks all known resouce-containing nodes on viability, 
	# sorts them in order of their distance and 
	# choose the closest one
	# go there
	def getKnownSourceFor(self, types):
		# just handling..
		if type(types)==int:
			types=(types,)
			
		# get all known sources for types
		appr=filter(lambda node: (node.resource and node.resource.type in (1,)), self.knownsources)
		if len(appr)>0:
			
			# choose nearest appropriate node
			dest=sorted(appr, key=lambda node: self.currentmapnode.distanceTo(node))[0]
			# go there
			print "go to known resource %d at [%d,%d]" % ((dest.resource.type,)+dest.location)
			self.pathfinder.find(self.getlocation(), dest.location)
			
			return dest
			
		else:
			return None
			
			


