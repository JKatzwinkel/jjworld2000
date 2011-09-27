class BFSHandler:


	def __init__(self):
	
		self.searching=False
		self.depth=0

		self.knownNodes=[]
		self.depthOfNodes=[]
		self.listPos=0
		
		self.lookingFor=0
		
		self.found=None
		
	
	# initialize a breadth-first-search from a specific node
	def find(self, startNode, lookingFor):
		
		self.searching=True
		if type(lookingFor)==int:
			lookingFor=(lookingFor,)
		self.lookingFor=lookingFor
		
		self.knownNodes=[]
		self.knownNodes.append(startNode)
		self.listPos=0
		self.depth=1
		self.depthOfNodes=[0]
		
		self.found=None
		
	
	# perform one step in BFS algorithm
	def search(self):

		if self.listPos < len(self.knownNodes):
			node=self.knownNodes[self.listPos]
		else:
			self.searching=False
			return
		
		# mark all neighbour nodes as to be searched
		for nn in node.neighbours:
			if not(nn in self.knownNodes):
				#check if whatever we are looking for is here
				if self.lookingFor is 0:
					if nn.coziness() > 10 or nn.resource and nn.resource.type is 0:
						self.found=nn
						self.searching=False
						print "bfs found acommodation in depth", self.depth, "@", self.found.location
						return
				else:
					if nn.resource and nn.resource.type in self.lookingFor and nn.resource.amount>0:
						self.found=nn
						self.searching=False
						print "bfs one of searched resources in depth %d @ %d,%d" % ((self.depth,) + self.found.location), self.lookingFor
						return
				
				# nothing found yet; continue			
				self.knownNodes.append(nn)
				self.depth=self.depthOfNodes[self.listPos]+1
				self.depthOfNodes.append(self.depth)
		
		self.listPos+=1
		
	# aborts search	
	def stop(self):
		
		self.searching=False
		
		
	# returns the discovered node and resets the corresponding field, so the algorithm can continue if nessessary
	def getFound(self):
		
		found=self.found
		self.found=None
		
		return found
		
