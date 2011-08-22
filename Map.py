import random
import numpy
import math

import Images

class Node:

	def __init__(self, location, lid, mp):
		self.map=mp
		self.neighbours=[]
		self.vegetation=random.random()*random.random()*random.random()*6
		self.water=0
		self.lid=lid
		self.location=location
		self.variant=random.randint(0,100)
		
	def cost(self):
		return 1+self.vegetation+self.water*20
	
	

class Map:

	

	def __init__(self, width, height):
		self.gfx = None
		self.width=width
		self.height=height

		
		self.nodes = []
		
		self.waternodes = []
		self.wavecounter=0
		
		
		for y in range(0,height):
			for x in range(0,width):
				self.nodes.append(Node((x,y), y*width+x, self))
		
		# connect nodes to their neighbours
		for n in self.nodes:
			for nn in self.getAdjacentNodes(n):
				n.neighbours.append(nn)
							
		# manage grass
		for i in range(0,2):
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
		pondsnr=width*height/400
		for i in range(0,random.randint(pondsnr,pondsnr*2)):
			towater=[]
			n=self.nodes[random.randint(0,len(self.nodes))]
			towater.append(n)
			counter=0
			
			while len(towater)>0 and counter<40:
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
		for i in range(0,random.randint(1,pondsnr/2)):
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
	def grow(self, times):
		for i in range(0,times):
			n=self.nodes[random.randrange(0,len(self.nodes))]
			if not(n.water>0):
				vsum=0
				old=int(n.vegetation)
				adj=n.neighbours
				for nn in adj:
					vsum+=nn.vegetation
				n.vegetation+=0.05+random.random()*vsum/len(adj)/20
				#only redraw square if its appearance has actually changed
				if int(n.vegetation)!=old:
					self.draw(n)
				
	# shrink, for instance when stepped on
	def shrink(self, node):
		old=int(node.vegetation)
		node.vegetation*=.9
		node.variant+=1
		if old>0: self.draw(node)
		
				
	# let water change image (wave effect!!!)
	def water_float(self, times):

		for i in range(0,times):
			n=self.waternodes[random.randrange(0,len(self.waternodes))]
			x,y=self.gfx.locationOnScreen(n)
			if not(y<0 or y>self.gfx.screensize[1]):
				if not(x<0 or x>self.gfx.screensize[0]):
					if (n.location[0]+n.location[1])%30==(self.wavecounter/5)%30:
						n.variant=random.randint(0,100)
						self.draw(n)
		self.wavecounter+=1	
	
	
	# draws square on gfx background and declares it to be updated on screen
	def draw(self, node):
		sprite=Images.getImage(node)
		x,y=node.location
		self.gfx.background.blit(sprite,(x*20,y*20))
		self.gfx.setDirty((x*20,y*20))	

