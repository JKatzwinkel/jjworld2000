import types
import random as rnd

import Jaja
import resources.Resource as rsc

import MentalMap



class Needs():



	def __init__(self, j):
	
		#dict(tuple, int)
		self.needs=[]
	
	
		self.hungry=.4
		self.thirsty=.4
		self.tired=.4
		
		self.jaja=j
		self.map=self.jaja.map

		self.memory=MentalMap.MentalMap(self.map)
		


		
	
	def update(self):
		
		if rnd.randint(0,20)<1:
			if self.jaja.action is Jaja.ACT_SLEEP:
				starve(self, .001)
				dry(self, .001)
			elif self.jaja.action is Jaja.ACT_STAND:
				starve(self, .002)
				dry(self, .002)
				exhaust(self, .002)
			elif self.jaja.action is Jaja.ACT_WALK:
				starve(self, .004)
				dry(self, .003)
				exhaust(self, .003)
				
				
		if self.memory.waiting():
			self.memory.update()
			
		

	# check what I need and if I can do sth about it
	def reflect(self):
	
		# spachteln
		if self.jaja.cnt > 60:			
			self.tryToConsume()
					

		self.needs=[]
		
		# for all basic body functions
		for f in functions:
			# check if critical:
			if sorrow[f](self) > .25:
				# look what resources are helping
				for res in remedies[f]:
					# check how strong their effect would be
					eff = rsc.effectivities[(res, f)]
					# check if its not too less and not too much
					if sorrow[f](self)*1.2 > eff > sorrow[f](self)/4:
						# check if other effects of the resource allow using it
						if rsc.isAppropriate(self, res):
							# add resource to list of wanted resources
							if not res in self.needs:
								self.needs.append(res)

		print "need resources ", self.needs						
					


	# if there is something where we stand, try to eat/drink/snort it
	# return true if successful
	def tryToConsume(self):
		mapnode=self.jaja.currentmapnode				
		if mapnode.resource:
			if mapnode.resource.amount>0:
				restype=mapnode.resource.type
				if restype in self.needs:
					if restype==0:
						self.sleep()
						return
					mapnode.resource.consume(self)
					return True
		return False



		
	# indicator for sublevel processing we will have to wait for
	def waiting(self):
		return self.memory.waiting()

				
	
	
	# method by which Jaja calls for directions
	def getDestination(self):
	
		# if there are resources we need to have
		if len(self.needs) > 0:
			# unless the mental map is currently making us wait...
			if not self.memory.waiting():
				# ... ask her for resources around
				print "attempt to get result list of resources around ", self.needs
				findings = self.memory.getResources(self.needs, self.jaja.currentmapnode.location)
				# if there are any:
				if findings:
					# if there are even any that can actually be used
					appropriates = filter(lambda n:rsc.isAppropriate(self, n.resource.type), findings)
					if len(appropriates)>0:
						# take the closest one of those
						node = sorted(appropriates, key=lambda n: self.jaja.currentmapnode.distanceTo(n))[0]
						# pass that one's position to Jaja
						print "passing dest node at ",node.location
						return node.location
						
				# if there are no known resources around, maybe we havent looked yet:
				else:
					# and should start a search at this point
					if self.memory.bff.startsearch(self.jaja.currentmapnode, self.needs):
						# if the search starts successfully, we will leave this method in order to await the search results
						return None


			# do we know a place where we can probably find those resources?
			print "attempt to retrieve known hot spot for res", self.needs
			spot = self.memory.closestspot(self.needs, self.jaja.currentmapnode.location)
			# is there such a place?
			if spot:
				# pass it to Jaja
				print "passing search spot at ",spot
				return spot
						


			# if there is no place known to be surrounded by those resources
		
			# ask the mental map for a nearby point where we will most likely be more lucky
			print "attempt to get a suggestion for where to go now"
			dest = self.memory.nextpos(self.needs, self.jaja.currentmapnode.location)
			# if available
			if dest:
				# pass it over to Jaja
				print "pass over new position ",dest
				return dest
				


		# if we dont need anything in particular
		# we will just stroll around and look for places where we can find useful resources
		else:
		
			# unless the mental map is busy
			if not self.memory.waiting():
				# ask for any useful resources around
				print "attempt to get any of all useful resources: ", rsc.usefulresources
				findings = self.memory.getResources(rsc.usefulresources, self.jaja.currentmapnode.location)
				# if there is a respond (only means that search has been performed without problems) 
				if findings:
					# ask the mental map for a nearby point where we can continue our search for whatever
					# there is always sth that isnt around, so like this, we can just go where the chance
					# is the best that we will find sth new
					print "attempt to get a suggestion for where to go next"
					dest = self.memory.nextpos(rsc.usefulresources, self.jaja.currentmapnode.location)
					# if available
					if dest:
						# pass it over to Jaja
						print "pass over new position ",dest
						return dest				
					
				else:
					# ok we should search 
					if self.memory.bff.startsearch(self.jaja.currentmapnode, rsc.usefulresources):
						return None
					# get place to go next without conducting a search before. why does this case happen even?
					else:
						print "attempt to get a suggestion for where to go next"
						dest = self.memory.nextpos(rsc.usefulresources, self.jaja.currentmapnode.location)
						# if available
						if dest:
							# pass it over to Jaja
							print "pass over new position ",dest
							return dest				
						
		
			
		return None	


			
			
			
	def sleep(self):
		# TODO: lieber methoden in Jaja machen fuer einpennen und so?
		self.jaja.action = Jaja.ACT_SLEEP
		self.jaja.cnt=0
		
	def consume(self):
		self.jaja.action = Jaja.ACT_CONSUME
		self.jaja.cnt=0


			
			
			
		
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
		
def dry(need, amount):
	need.thirsty=min(1, need.thirsty+amount)
	

	
# get better
def eat(need, amount):
	need.hungry=max(0, need.hungry-amount)
		
def recreate(need, amount):
	need.tired=max(0, need.tired-amount)
		
def drink(need, amount):
	need.thirsty=max(0, need.thirsty-amount)
			
	
# get values
def hunger(need):
	return need.hungry
	
def thirst(need):
	return need.thirsty
	
def tiredness(need):
	return need.tired
	
sorrow = {eat:hunger, drink:thirst, recreate:tiredness}
functions=[eat, drink, recreate]
			


