import types
import random as rnd

import Jaja

class Needs:

	def __init__(self, j):
	
		#dict(tuple, int)
		self.needs={}
		
		self.knownresources={}
	
		self.hungry=.7
		self.thirsty=.7
		self.tired=.7
		
		self.jaja=j
		self.map=self.jaja.map
		
	
	def update(self):
		
		if rnd.randint(0,20)<1:
			if self.jaja.action is Jaja.ACT_SLEEP:
				starve(self, .001)
				thirst(self, .001)
			elif self.jaja.action is Jaja.ACT_STAND:
				starve(self, .002)
				thirst(self, .002)
				exhaust(self, .002)
			elif self.jaja.action is Jaja.ACT_WALK:
				starve(self, .003)
				thirst(self, .003)
				exhaust(self, .003)
			
	
	# check what I need and if I can do sth about it
	def reflect(self):
	
		mapnode=self.jaja.currentmapnode
		
		if mapnode.resource:
			if mapnode.resource.amount>0:
				restype=mapnode.resource.type
				for need in self.needs.items():
					if restype in need[0]:
						mapnode.resource.consume(self)
						del(self.needs[need[0]])
						break
			else:
				try:
					del(self.knownresources[mapnode])
				except:
					pass
				

		if self.thirsty>.3:
			self.urge(remedies[drink])
		
		if self.hungry>.4:
			self.urge(remedies[eat])
			
		if self.tired>.4:
			if mapnode.coziness()>20 and not(mapnode.resource):
				self.sleep()
			else:
				self.urge(remedies[recreate])
			
			
			
	def sleep(self):
		# TODO: lieber methoden in Jaja machen fuer einpennen und so?
		self.jaja.action = Jaja.ACT_SLEEP
		self.jaja.cnt=0
		
	def consume(self):
		self.jaja.action = Jaja.ACT_CONSUME
		self.jaja.cnt=0

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
			
			
	# saves a list of sources (tuple)
	def memorizeSources(self, sources):
		for i in sources:
			self.knownresources[i[0]]=i[1]
			
	
	# returns the closest known resource for a certain purpose (eg eat...)
	# TODO: nur die quellen zurueckgeben, die auch ausreichend effekt auf die jeweilige funktion haben
	def closestSource(self, purp):
		if len(self.knownresources)>0:
			mapnode=self.jaja.currentmapnode
			
			if type(purp) is types.FunctionType:
				func = lambda n: remedies[purp][n[0].resource.type]==True and n[1]>0
			elif  type(purp) is types.TupleType:
				func = lambda n: n[0].resource.type in purp and n[1]>0
				
			usefulsources = filter(func, self.knownresources.items())
			if len(usefulsources) > 0:
				return sorted(usefulsources, key=lambda n:n[0].distanceTo(mapnode))[0][0]
			else:
				return None
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
	need.hungry=min(1, need.hungry+amount)
	
def exhaust(need, amount):
	need.tired=min(1, need.tired+amount)
		
def thirst(need, amount):
	need.thirsty=min(1, need.thirsty+amount)
	

	
# get better
def eat(need, amount):
	need.hungry=max(0, need.hungry-amount)
		
def recreate(need, amount):
	need.tired=max(0, need.tired-amount)
		
def drink(need, amount):
	need.thirsty=max(0, need.thirsty-amount)
			
	
	
			
	
