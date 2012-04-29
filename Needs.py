import Jaja

class Needs:

	def __init__(self, j):
	
		#dict(tuple, int)
		self.needs={}
		
		self.knownresources={}
	
		self.hungry=0
		self.thirsty=0
		self.tired=0
		
		self.jaja=j
		self.map=self.jaja.map
		
	
	def update(self):
		
		if self.jaja.action is Jaja.ACT_SLEEP:
			starve(self, .0001)
			thirst(self, .0001)			
		elif self.jaja.action is Jaja.ACT_STAND:
			starve(self, .0002)
			thirst(self, .0002)
			exhaust(self, .0002)
		elif self.jaja.action is Jaja.ACT_WALK:
			starve(self, .0003)
			thirst(self, .0003)
			exhaust(self, .0003)
			
	
	# check what I need and if I can do sth about it
	def reflect(self):
	
		mapnode=self.jaja.currentmapnode
		
		# TODO: schlafen!
		if mapnode.resource:
			restype=mapnode.resource.type
			for need in self.needs.items():
				if restype in need[0]:
					mapnode.resource.consume(self)
					del(self.needs[need[0]])
					break
				

		#TODO: die liste der resourcen, die gebraucht werden, als priority list oder so bauen

		if self.thirsty>.7:
			self.urge(remedies[drink])
		
		if self.hungry>.5:
			self.urge(remedies[eat])
			
		if self.tired>.7:
			self.urge(remedies[recreate])
			
		

	# returns the set of resources which are needed most urgently (highest priority value)
	# and removes it from the list
	def urgent(self):
		if len(self.needs)>0:
			first = sorted(self.needs, key=lambda r: self.needs[r])[len(self.needs)-1]
			del self.needs[first]
			print "most urgent set of res:", first
			return first
		else:
			return None
			
	
	
	# increases the prioroty for a certain set (tuple) of resources by n
	def urge(self, rem, n=1):
		try:
			self.needs[tuple(rem)]+=n
		except:
			self.needs[tuple(rem)]=n
			

	# saves map node where to find resource			
	def memorizeSource(self, node):
		if node.resource:
			self.knownresources[node]=node.resource.amount
		else:
			print "can't memorize source: no resource"
			
			
	# saves a list of sources
	def memorizeSources(self, sources):
		for i in sources.items():
			self.knownresources[i[0]]=i[1]
			
	
	# returns the closest known resource for a certain purpose (eg eat...)
	def closestSource(self, purp):
		if len(self.knownresources)>0:
			mapnode=self.jaja.currentmapnode
			if type(purp) is types.FunctionType:
				usefulsources = filter(lambda n: remedies[purp][n.resource.type]==True, self.knownsources)
				closest = sorted(usefulsources, key=lambda n:n.distanceTo(mapnode))[0]
				return closest
			elif type(purp) is types.TupleType:
				usefulsources = filter(lambda n: n.resource.type in purp, self.knownsources)
				closest = sorted(usefulsources, key=lambda n:n.distanceTo(mapnode))[0]
		else:
			return None
			
			
		
# TODO: vielleicht nach Resources.py
# what resources bring effect on what purpose: dict(function, tuple)
remedies={}

def register(restype, effect):
	print "Register function/resource", effect, restype
	try:
		print "remedies for ", effect, ": ", remedies[effect]
		remedies[effect][restype]=True
	except:
		remedies[effect]={restype:True}
	print "remedies for ", effect, ": ", remedies[effect]
	
		
		
# get worse
def starve(need, amount):
	if need.hungry<1:
		need.hungry+=amount
	else:
		need.hungry=1
	
def exhaust(need, amount):
	if need.tired<1:
		need.tired+=amount
	else:
		need.tired=1
		
def thirst(need, amount):
	if need.thirsty<1:
		need.thirsty+=amount
	else:
		need.thirsty=1
	

	
# get better
def eat(need, amount):
	if need.hungry>0:
		need.hungry=max(0, need.tired-amount)
	else:
		need.hungry=0
		
def recreate(need, amount):
	if need.tired>0:
		need.tired=max(0, need.tired-amount)
	else:
		need.tired=0
		
def drink(need, amount):
	if need.thirsty>0:
		need.thirsty=max(0, need.tired-amount)
	else:
		need.thirsty=0
			
	
	
			
	
