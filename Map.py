import random, numpy


class Node:

	def __init__(self, location, lid):
		self.neighbours=[]
		self.vegetation=random.random()*random.random()*random.random()*5
		self.lid=lid
		self.location=location
		self.variant=random.randint(0,100)
		


class Map:

	

	def __init__(self, width, height):
		self.width=width
		self.height=height

		
		self.nodes = []
		
		for y in range(0,height):
			for x in range(0,width):
				self.nodes.append(Node((x,y), y*width+x))
		
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
			
				
			
	def getNode(self, location):
		x,y=location
		if x<0: return None
		if x>=self.width: return None
		if y<0: return None
		if y>=self.height: return None
		return self.nodes[y*self.width+x]
		
	
	def getAdjacentNodes(self, node):
		result=[]
		x,y=node.location
		#for ny in range(y-1,y+2):
		#	for nx in range(x-1,x+2):
		#		if ny>=0 and  ny<self.height:
		#			if nx>=0 and nx<self.width:
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
		

