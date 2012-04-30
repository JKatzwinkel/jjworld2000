# -*- coding: latin-1 -*-
import pygame
from random import randint as rnd
import math
import operator

import Pathfinder
import Images
import BFSHandler
import Needs


ACT_SLEEP=0
ACT_STAND=1
ACT_WALK=2

# zwei ebenen trennen? state fuer schlafen, stehen, gehen und action für trinken, suchen, oder aehnliches?
ACT_CONSUME=3


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
		
		self.areaOnScreen=None
		
		self.pathfinder=Pathfinder.Pathfinder(self.map)
		self.path=[]
		self.direction=1
		
		self.bfs=BFSHandler.BFSHandler()
		
		# TODO
		self.knownsources=[]
		self.nearestknownsource=None
		
		self.action=ACT_STAND
		
		self.needs=Needs.Needs(self)
		
		#counter
		self.cnt=0
		

		
	
		
	
	# method to be called in every loop
	# calls the move-method which updates the position of the character
	def update(self):
		
		self.cnt+=1

		self.needs.update()

		# sleep		
		if self.action is ACT_SLEEP:
			Needs.recreate(self.needs, .001+self.currentmapnode.vegetation*.001)
			# TODO: auslagern?
			if self.needs.tired<.1:
				self.action=ACT_STAND
			
			
		elif self.action is ACT_CONSUME:
			if self.cnt>50:
				self.action=ACT_STAND

			
		# stand
		elif self.action is ACT_STAND:
			
		
			# if there is not a* search running
			if not self.pathfinder.searching:


				# if there is not already a path that I could walk
				if not len(self.path) > 0:
					# get path from a* handler
					path=self.pathfinder.getPath()
					# if path available:
					if path:
				
						self.path=path
						self.action=ACT_WALK
					# if no path available yet	
					else:
						# if there is no breadth first search running
						if not self.bfs.searching:
					
							# check what I feel to need and act like this
							self.needs.reflect()
					
							found=self.bfs.getFound()
							# if bfs did already return a destiny, stop search (???TODO) and start a* to that certain node
							if found: 
								
								self.bfs.stop()
								self.pathfinder.find(self.currentmapnode.location, found.location)
								
								
							# if I need sth, start looking for the most urgent thing
							elif len(self.needs.needs)>0:
							
								need = self.needs.urgent()
								#print "go find resource ", need
								self.bfs.find(self.currentmapnode, need)		
								
							# if I dont need anything, just go somewhere
							else: 
								if rnd(0,100) < 1:
									self.goAnyWhere()
								
						
						# if there is currently a bfs running
						else:
							
							# get the position of the closest known source for a certain need
							if not self.nearestknownsource:
								self.nearestknownsource = self.needs.closestSource(self.bfs.lookingFor)
							
							# if the bfs takes too long, either go to the closest known source or, if there aint one, just wander around
							# TODO
							if self.nearestknownsource and self.bfs.depth*3 > self.nearestknownsource.distanceTo(self.currentmapnode)*2 or self.bfs.depth>15:
								
								self.bfs.stop()
								self.needs.memorizeSources(self.bfs.getSpotted())
								
								if self.nearestknownsource:
									#print "bfs takes too long, go to known resource @ ", self.nearestknownsource.location
									self.pathfinder.find(self.currentmapnode.location, self.nearestknownsource.location)
									self.nearestknownsource=None
									
								else:
									self.goAnyWhere()
									
						
							if rnd(0,25)<1:
								self.direction=1+2-self.direction

				
								

			# conduct limited steps of a*-algorithm path search
			if self.pathfinder.searching:
				self.pathfinder.search()
			elif self.bfs.searching:
			# conduct steps in bfs algorithm if no a* running
				self.bfs.search()


		# walk
		elif self.action is ACT_WALK:
			self.move()

		# set the background range which has been occupied by the character as to be redrawn
		if self.areaOnScreen:
			self.map.gfx.setDirty(self.areaOnScreen)		
		
	
	# take care of movement
	def move(self):
		x,y=self.location
		nx,ny=self.currentmapnode.location
		
		# to be opt
		if x>=nx+.5 or x<=nx-.5 or y>=ny+.5 or y<=ny-.5:
			# TODO returns null???
			self.currentmapnode=self.map.getNode(self.getlocation())
			self.map.shrink(self.currentmapnode)
		
		
		if len(self.path)>0:
			#print len(self.path)
			
			dest=self.path[len(self.path)-1]
			dx,dy=dest.location
			
			mx=dx-x
			my=dy-y
			rad=math.hypot(mx,my)			
			
			
			if rad>.1:
				cost=self.currentmapnode.cost()
				speed=.2/cost * (1.1-self.needs.tired)
				mx/=rad
				my/=rad
				x+=mx*speed
				y+=my*speed
				self.location=(x,y)
				
				Needs.exhaust(self.needs, self.needs.hungry*cost/10000)
				
				if mx>0:
					self.direction=1
				else:
					self.direction=2
			else:
				self.path.pop()
		else:
			self.action=ACT_STAND
				
				
			
	# draw the punk to the given surface
	def draw(self, surface, relative=True):

		location=map(operator.mul, self.location, (20,20))
		self.areaOnScreen=pygame.Rect(location, (20,22))
		
		los=self.locationOnScreen(relative)

		if not(self.currentmapnode.water>0):
			surface.blit(Images.getJajaImage(self), los)
		else:
			x,y=los
			surface.blit(Images.getJajaImage(self), (x,y), (0,0,20,12))
			
		
		if self.pathfinder.searching:
			pos=map(operator.add,los,(-9,-7))
			surface.blit(Images.getIconImage(Images.ICON_BUBBLE), pos)

			self.areaOnScreen=pygame.Rect(map(operator.add, location, (-9,-7)), (29,27))
			
		# TODO: balken!
		pygame.draw.line(surface, (200,0,0), los, map(operator.add, los, (int(19-self.needs.tired*19),0) ))
		pygame.draw.line(surface, (0,200,0), map(operator.add,los,(0,1)), map(operator.add, los, (int(19-self.needs.hungry*19),1) ))
		pygame.draw.line(surface, (0,0,200), map(operator.add,los,(0,2)), map(operator.add, los, (int(19-self.needs.thirsty*19),2) ))




	# compute the position relative to the screen's position
	def locationOnScreen(self, relative=True):
	
		x,y=self.location
		if relative:
			sx,sy=self.map.gfx.topleft
		else:
			sx,sy=(0,0)
		x=x*20-sx
		y=y*20-sy+int(self.currentmapnode.water>0)*2
		return (int(x),int(y))
		
	
		



	# determine the map square on which the character is currently standing on 	
	# possibly TODO	
	def getlocation(self):
		return (int(round(self.location[0])), int(round(self.location[1])))
		
		

	# just find a random destination of close distance that is easy to walk and dry
	# start finding a path to there using a*	
	# TODO can possibly hang up
	def goAnyWhere(self, distance=6):
	
		jx,jy=self.currentmapnode.location
		x,y=(rnd(jx-distance,jx+distance),rnd(jy-distance,jy+distance))
		node=self.map.getNode((x,y))
		veg=3
		while not(node) or node.water>0 or node.vegetation>veg or node.resource:
			x,y=(rnd(jx-distance,jx+distance),rnd(jy-distance,jy+distance	))
			node=self.map.getNode((x,y))
			veg+=.1
			if rnd(0,10)<1:
				distance+=1

		self.pathfinder.find(self.getlocation(), (x, y))
		
		
		
	# checks all known resouce-containing nodes on viability, 
	# sorts them in order of their distance and 
	# choose the closest one
	# go there !!!!
#	def getKnownSourceFor(self, types):
#		# just handling..
#		if type(types)==int:
#			types=(types,)
#			
#		# get all known sources for types
#		appr=filter(lambda node: (node.resource and node.resource.type in types), self.knownsources)
#		
#		if len(appr)>0:
#			
#			# choose nearest appropriate node
#			dest=sorted(appr, key=lambda node: self.currentmapnode.distanceTo(node))[0]
#			# go there
#			
#			return dest
#			
#		else:
#			return None
#			
	
#	# stores node known as source in the known-sources list
#	def memorizeSource(self, node):
#	
#		if not node in self.knownsources:
#			self.knownsources.append(node)
#			
#			
#	# deletes node from known-sources list
#	def forgetSource(self, node):
#		if node in self.knownsources:
#			self.knownsources.remove(node)
			
			
#	# checks if certain resource is needed:
#	def isNeeded(self, res):
#	
#		if type(res)==int:
#			res=(res,)
#			
#		for n in self.needs:
#			if any(map(lambda x: x in res, n)):
#				return True
				
#		return False
			
			
	# remember that I need something
#	def need(self,res):
#		
#		if self.isNeeded(res):
#			return 
#		
#		if type(res)==int:
#			res=(res,)
#		
#		self.needs.append(res)
		
		
		
	# think about what would be good for me
#	def think_n_act(self):

		# decide what to do and what to need	
#		self.needs.reflect()
#		return
	
		# tired
#		if self.tired > .6:
#			if self.currentmapnode.containsResources(0):
#				#print "found pillow"
#				self.memorizeSource(self.currentmapnode)
#				self.action=Jaja.ACT_SLEEP
#			elif self.currentmapnode.resource is None and self.currentmapnode.coziness()>10:
#				#print "found place to sleep: ", self.currentmapnode.coziness()
#				self.action=Jaja.ACT_SLEEP
#				if self.currentmapnode.coziness()>50:
#					self.currentmapnode.spawnResource(0,1)
#					self.memorizeSource(self.currentmapnode)
#
#			else :
#				self.need(0)
#	
#		# hungry	
#		# TODO: essen, trinken, schlafen, etc alles auslagern in externe klasse needs oder so, dann kann da alles erledigt werden und hier
#		# werden dann aliase fuer die entsprechenden funktionen aufgerufen
#		elif self.hunger >.6:
#			if self.currentmapnode.containsResources((1,2)):
#				if self.currentmapnode.resource.consume():
#					#print "found something to eat: ", self.currentmapnode.resource.type
#					self.memorizeSource(self.currentmapnode)
#					self.hunger -= self.currentmapnode.resource.effectivity
#				else:
#					self.forgetSource(self.currentmapnode)
#			else :
#				self.need((1,2))
#		
#		# bored
#		elif self.tired < .2 and self.hunger < .8:
#			if self.currentmapnode.containsResources(1):
#				if self.currentmapnode.resource.consume():
#					#print "betrinking"
#					# TODO: der ganze resourcenkram muß woanders hin
#					self.memorizeSource(self.currentmapnode)
#					self.hunger -= self.currentmapnode.resource.effectivity/2
#					self.goAnyWhere(2)
#				else:
#					self.forgetSource(self.currentmapnode)
#			else:
#				self.need(1)
