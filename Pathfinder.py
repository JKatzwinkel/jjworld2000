class PathNode:


	def __init__(self, node, parent, cost):
		self.parent=parent
		self.node=node
		self.cost=cost
		
				

class Pathfinder:
	
	
	def __init__(self, mp):
		
		self.map=mp
		
		self.open=[]
		self.openlid=[]
		self.closed=[]
		self.searching=False
		
		self.dest=None
		self.path=[]
		
		
	# returns node object for search graph
	def pathNode(self, node, parent):

		if parent:
			g=parent.cost
		else:
			g=0
		
		dx,dy=self.dest.location
		x,y=node.location
		
		h = abs(dx-x)+abs(dy-y)
		
		f = g + int(node.cost()-1)*20 + h
		
		return PathNode(node, parent, f)	
		
		
		
	# initialize a* algorithm
	def find(self, start, dest):

		if len(self.open)>0: return
#		print "starting path search from", start, "to", dest
		
		self.open=[]
		self.openlid=[]
		self.closed=[]
		
		self.searching=True
		
		self.dest=self.map.getNode(dest)
		self.path=[]

		startnode=self.map.getNode(start)
		self.open.append(self.pathNode(startnode, None))
		self.openlid.append(startnode.lid)
		
		
	# conduct one step in a* algorithm
	def search(self):
	
		if len(self.open)==0: 
			self.searching=False
			return
		
		pn=min(self.open, key=lambda node: node.cost)

		if pn.node.location==self.dest.location:
			#print "FOUND ", pn.node.location
			self.path.append(pn.node)
			while pn:
				self.path.append(pn.node)
				pn=pn.parent
			self.open=[]
			return
		
		for nn in pn.node.neighbours:
		
			if not(nn.lid in self.closed):
				newnode=self.pathNode(nn,pn)
				
				if not(nn.lid in self.openlid):
					self.open.append(newnode)
					self.openlid.append(nn.lid)
				else:
					oldnode=self.open[self.openlid.index(nn.lid)]
					if newnode.cost<oldnode.cost:
						print "better path found"
						oldnode.cost=newnode.cost
						oldnode.parent=newnode.parent
			

		self.open.remove(pn)
		self.openlid.remove(pn.node.lid)
			
		self.closed.append(pn.node.lid)

	
	# return complete path
	def getpath(self):
	
		if len(self.path)>0:
			return self.path
		return None
		
	
