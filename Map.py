import random
import numpy
import math
import pygame
import operator

import Images
import resources.ResourceFactory as Rsc

class Node:

	def __init__(self, location, lid, mp):
	
		self.map=mp
		self.neighbours=[]
		self.vegetation=random.random()*random.random()*random.random()*random.random()*12
		self.water=0
		self.lid=lid
		self.location=location
		self.variant=random.randint(0,100)		
		self.resource=None
		#TODO: self.cost
		
	
	# returns the difficulty level of moving on this map node. 
	# used to determine the speed of moving characters
	# and in shortest path algorithm
	# TODO: avoid calculation the cost that often. do this only if it actually might change
	def cost(self):
		return 1+self.vegetation+self.water*14+float(not self.resource is None)*2.5
		
	
	# returns the (manhattan) distance to the given node
	def distanceTo(self, node):
		x,y=tuple(map(operator.sub, self.location, node.location))
		return abs(x)+abs(y)
		
		
	# returns the sum of this node's vegetation level plus its neighbours'. 
	# used to determine vegetation growing speed
	def fertility(self):
		vsum=sum(map(lambda nn : nn.vegetation+nn.water*5+int(nn.containsResources(2)), self.neighbours))
		return vsum+self.vegetation

	# an indicator for how comfortable a place is to sleep on
	def coziness(self):
		if self.vegetation<1 or self.water>0:
			return 0
		vsum=reduce(lambda x,y: x*y, (map(lambda nn : max(nn.water*1.5, min(nn.vegetation**2, nn.vegetation+.5)), self.neighbours)))
		return vsum*self.vegetation

	# draws node in current appearance on surface
	# also returns absolute coordinates of the node, if something wants it	
	def draw(self, surface):
		sprite=Images.getMapNodeImage(self)
		x,y=map(operator.mul, self.location, (20,20))
		surface.blit(sprite, (x,y))
		return x,y
	
	
	# spawns a certain resource on this very map node
	def spawnResource(self, restype, amount):
		if self.resource is None:
			self.resource = Rsc.createResource(restype, amount, self)
			self.resource.draw(self.map.gfx.layer)
#			self.map.gfx.setDirty(self)
			
		
	# tells if there is a resoucre of a certain kind on this node
	# this resource may even be empty !!!	
	def containsResources(self, restypes):
		if type(restypes) is int:
			restypes=(restypes,)
		if self.resource:
			if self.resource.type in restypes:
				return True
		return False

			

class Map:

	

	def __init__(self, width, height):
		self.gfx = None
		self.width=width
		self.height=height

		
		self.nodes = []
		
		self.waternodes = []
		self.wavecounter=0
		
		# initialize map node list
		for y in range(0,height):
			for x in range(0,width):
				self.nodes.append(Node((x,y), y*width+x, self))
		
		# connect nodes to their neighbours
		for n in self.nodes:
			for nn in self.getAdjacentNodes(n):
				n.neighbours.append(nn)
							
		# manage grass
		for i in range(0,5):
			vegetation=numpy.zeros(len(self.nodes))
			for n in self.nodes:
				vsum=0
				adjNodes=n.neighbours
				for nn in adjNodes:
					vsum+=nn.vegetation
				vegetation[n.lid]=vsum/len(adjNodes)
			
			for n in self.nodes:
				n.vegetation=vegetation[n.lid]
		
		# create ponds
		pondsnr=width*height/500
		for i in range(0,random.randint(pondsnr,pondsnr*2)):
			towater=[]
			n=self.nodes[random.randrange(0,len(self.nodes))]
			towater.append(n)
			counter=0
			
			while len(towater)>0 and counter<random.randint(40,70):
				counter+=1
				n=towater.pop(0)
				n.water=1
				n.vegetation=0
				if not(n in self.waternodes):
					self.waternodes.append(n)
				for nn in n.neighbours:
					if random.random()<.5:
						if not(nn in towater or nn.water>0):
							towater.append(nn)
			
		# creeks
		for i in range(0,random.randint(3,pondsnr/2)):
			creeknodes=[]
		
			if random.random()<.5:
				x=random.randint(0,(self.width-1))
				y=random.randint(0,1)*(self.height-1)
			else:
				x=random.randint(0,1)*(self.width-1)
				y=random.randint(0,(self.height-1))
			print x,y
			deg=math.atan2((self.height/2-y),(self.width/2-x))
			deg0=deg
		
			while not(x<0 or x>self.width or y<0 or y>self.height):
				node=self.getNode((int(round(x)),int(round(y))))
				if node in self.waternodes: 
					break
				if node:
					node.water=1
					if not(node in creeknodes):
						creeknodes.append(node)
				x+=math.cos(deg)*.1
				y+=math.sin(deg)*.1
				deg+=random.random()*.2-.1
				if deg>deg0+math.pi/2: deg=deg0+math.pi/2
				if deg<deg0-math.pi/2: deg=deg0-math.pi/2
			
			for n in creeknodes:
				self.waternodes.append(n)
				
		
		# let more grass grow on nodes adjacent to those holding water
		for n in self.nodes:
			if n.water==0:
				n.vegetation+=sum(map(lambda nn : nn.water, n.neighbours))
				
		
		
		


	# do some gardening
	def initDetails(self):
		
		# grow some groups of bushes
		
		for i in range(0,random.randrange(2,self.height*self.width/600)):
			n=self.nodes[random.randint(0,len(self.nodes))]
			while n.fertility() < 4 or n.fertility()>10 or n.water>0 or n.resource or n.vegetation<1:
				n=self.nodes[random.randrange(0,len(self.nodes))]
			
			for j in range(0,random.randrange(20,50)):
				if n.water==0 and n.fertility()>3 and n.fertility()<10:
					n.spawnResource(2,random.randrange(0,5))
					n.vegetation+=1
				n=n.neighbours[random.randrange(0,len(n.neighbours))]		


							
		
				
	# returns the node at the given location
	def getNode(self, location):
		x,y=location
		if x<0: return None
		if x>=self.width: return None
		if y<0: return None
		if y>=self.height: return None
		return self.nodes[y*self.width+x]
		
		
	# returns the node the id of which fits the given one
	def getNodeByID(self, lid):
		if lid<0: return None
		if lid>=len(self.nodes): return None
		return self.nodes[lid]
		
		
	# returns the (up to four) nodes which are directly adjacent to the given one
	# the result should be stored in the Node's field neighbours instead of calling this method all the time
	def getAdjacentNodes(self, node):
		result=[]
		x,y=node.location

		for nx in range(x-1,x+2,2):
			n = self.getNode((nx,y))
			if n: result.append(n)
		for ny in range(y-1,y+2,2):
			n = self.getNode((x,ny))
			if n: result.append(n)
		return result
		
		
	# let some grass grow
	# or resources
	def grow(self, times):
		for i in range(0,times):
			n=self.nodes[random.randrange(0,len(self.nodes))]

			if not(n.vegetation>6):
				old=int(n.vegetation)
				n.vegetation += 0.01 + random.random() * n.fertility() / 40
				#only redraw square if its appearance has actually changed
				if int(n.vegetation)!=old:
					n.draw(self.gfx.background)
				
			if n.resource:
				n.resource.grow()
				n.resource.draw(self.gfx.layer)
			
			elif n.vegetation>1.4:
				fertility=n.fertility()
				if fertility>7.2 and fertility<9.2 and (random.random()<.01 or any(map(lambda nn: nn.containsResources(2), n.neighbours))):
					n.spawnResource(2,0)
					
				
	# shrink, for instance when stepped on
	def shrink(self, node):
		old=int(node.vegetation)
		node.vegetation*=.85
		node.variant+=1
		if old>0: 
			node.draw(self.gfx.background)
			self.gfx.setDirty(node)
				
				
	# let water change image (wave effect!!!)
	def water_float(self, times):

		for i in range(0,times):
			n=self.waternodes[random.randrange(0,len(self.waternodes))]
			x,y=self.gfx.locationOnScreen(n)
			if not(y<0 or y>self.gfx.screensize[1]):
				if not(x<0 or x>self.gfx.screensize[0]):
					if (n.location[0]+n.location[1])%30==(self.wavecounter/5)%30:
						n.variant=random.randint(0,100)
						n.draw(self.gfx.background)
						self.gfx.setDirty(n)
		self.wavecounter+=1	
	

