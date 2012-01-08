class PathNode:


	def __init__(self, node, parent, cost):
		self.parent=parent
		self.node=node
		self.cost=cost
		
				

class Pathfinder:
	
	
	def __init__(self, mp):
		
		self.map=mp
		
		self.open={}
		self.closed={}
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
		
		# TODO: rather than arrays, use dictionaries
		self.open={}
		self.closed={}
		
		self.searching=True
		
		self.dest=self.map.getNode(dest)
		self.path=[]

		startnode=self.map.getNode(start)
#		self.open.append(self.pathNode(startnode, None))
		self.open[startnode.lid]=self.pathNode(startnode, None)
		
		
	# conduct one step in a* algorithm
	def search(self):
	
		if len(self.open)==0: 
			self.searching=False
			return
		
#		pn=min(self.open, key=lambda node: node.cost)
		pn=min(self.open.values(), key=lambda node: node.cost)

		if pn.node.location==self.dest.location:
			#print "FOUND ", pn.node.location
			self.path.append(pn.node)
			while pn:
				self.path.append(pn.node)
				pn=pn.parent
			self.open=[]
			self.searching=False
			return
		
		
		for nn in pn.node.neighbours:
		
			try:
				self.closed[nn.lid]
			# if lID not in closed list so far:
			except KeyError:
		
				newnode=self.pathNode(nn,pn)
				
				try:
					if newnode.cost < self.open[nn.lid].cost:
						#print "better path found"
						self.open[nn.lid] = newnode
				except KeyError:
					self.open[nn.lid] = newnode
				

		del self.open[pn.node.lid]
			
		self.closed[pn.node.lid]=True

	
	# return complete path
	def getPath(self):
	
		if len(self.path)>0:
			return self.path
		return None
		
	
