class BFSHandler:


	def __init__(self):
	
		self.searching=False
		self.depth=0

		self.knownNodes={}
		self.nodesToGo=[]
		
		self.lookingFor=0
		
		self.found=None
		
	
	# initialize a breadth-first-search from a specific node
	def find(self, startNode, lookingFor):
		
		self.searching=True
		if type(lookingFor)==int:
			lookingFor=(lookingFor,)
		self.lookingFor=lookingFor
		
		self.knownNodes={startNode.lid:0}
		self.nodesToGo=[startNode]
		self.depth=0
		
		# resources found accidently while looking for something
		self.spotted={}
		
		self.found=None
		
	
	# perform one step in BFS algorithm
	def search(self):

		if len(self.nodesToGo)>0:
			node=self.nodesToGo.pop(0)
			self.depth=self.knownNodes[node.lid]
		else:
			self.searching=False
			return
		
		# mark all neighbour nodes as to be searched
		for nn in node.neighbours:
			try:
				self.knownNodes[nn.lid]
			# if neighbour node is not known yet
			except KeyError:

				#check if whatever we are looking for is here
				if 0 in self.lookingFor:
					if nn.coziness() > 20 or nn.resource and nn.resource.type is 0:
						self.found=nn
						self.searching=False
						#print "bfs found acommodation in depth", self.depth, "@", self.found.location
						return
				else:
					if nn.resource:
						self.spotted[nn]=nn.resource.amount
						if nn.resource.type in self.lookingFor and nn.resource.amount>0:
							self.found=nn
							self.searching=False
							#print "bfs one of searched resources in depth %d @ %d,%d" % ((self.depth,) + self.found.location), self.lookingFor
							return
				
				# nothing found yet; continue			
				self.nodesToGo.append(nn)
				self.knownNodes[nn.lid]=self.depth+1
		

		
	# aborts search	
	def stop(self):
		
		self.searching=False
		
		
	# returns the discovered node and resets the corresponding field, so the algorithm can continue if nessessary
	def getFound(self):
		
		found=self.found
		self.found=None
		
		return found
		
		
	# returns a list of tuples for all spotted resources
	def getSpotted(self):
		return self.spotted.items()
		
