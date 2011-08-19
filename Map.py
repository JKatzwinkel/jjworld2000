import random, numpy


class Node:

	def __init__(self, location, lid, mp):
		self.map=mp
		self.neighbours=[]
		self.vegetation=random.random()*random.random()*random.random()*6
		self.lid=lid
		self.location=location
		self.variant=random.randint(0,100)
	
	def render(self):
		x,y=self.map.gfxHandler.locationOnScreen(self)
		if not(y<-40 or y>self.map.gfxHandler.screensize[1]+40):
			if not(x<-40 or x>self.map.gfxHandler.screensize[0]+40):
				image=self.map.gfxHandler.sprites.getSprite(self)
				if not(image):
					image=pygame.Surface((20,20))
					image.fill((255,255,255))
				image.rect = pygame.Rect(x,y,20,20)
				self.map.gfxHandler.demandToBeDrawn(image)
				
	def setDirty(self):
		if self.map.gfxHandler:
			x,y=self.map.gfxHandler.locationOnScreen(self)
			if not(y<-40 or y>self.map.gfxHandler.screensize[1]+40):
				if not(x<-40 or x>self.map.gfxHandler.screensize[0]+40):
					self.map.dirty.append(self.lid)
		else:
			if not(self.lid in self.map.dirty):
				self.map.dirty.append(self.lid)
		

class Map:

	

	def __init__(self, width, height):
		self.gfxHandler = None
		self.width=width
		self.height=height
		self.dirty=[]

		
		self.nodes = []
		
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
		
		# set all nodes dirty
		for n in self.nodes:
			n.setDirty()
			
				
			
	def getNode(self, location):
		x,y=location
		if x<0: return None
		if x>=self.width: return None
		if y<0: return None
		if y>=self.height: return None
		return self.nodes[y*self.width+x]
		
	def getNodeByID(self, lid):
		if lid<0: return None
		if lid>=len(self.nodes): return None
		return self.nodes[lid]
		
	
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
		
		
	def grow(self, times):
		for i in range(0,times):
			n=self.nodes[random.randrange(0,len(self.nodes))]
			vsum=0
			adj=n.neighbours
			for nn in adj:
				vsum+=nn.vegetation
			n.vegetation+=0.1+random.random()*vsum/len(adj)/10
			#n.setDirty()
			sprite=self.gfxHandler.sprites.getSprite(n)
			x,y=n.location
			self.gfxHandler.background.blit(sprite,(x*20,y*20))
			self.gfxHandler.setDirty((x*20,y*20))
			
			
			
	def draw(self, surface, clean=False):
		for lid in self.dirty:
			n = self.getNodeByID(lid)
			
			x,y=self.gfxHandler.locationOnScreen(n)
			w,h=self.gfxHandler.screensize
			
			if not(y<-20-20 or y>=h+20):
				if not(x<-20-20 or x>=w+20):
					if clean: self.dirty.remove(lid)
					sprite=self.gfxHandler.sprites.getSprite(n)
					if sprite:
						surface.blit(self.gfxHandler.sprites.getSprite(n), (x,y))#pygame.Rect(x,y,20,20))

		

