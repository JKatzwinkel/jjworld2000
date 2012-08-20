import random as rnd
import KDTree as kd
import operator
import pygame
import resources.Resource as rsc

# breadth first finder
class BFF():

	def __init__(self):
	
		self.start=None
		self.known={}
		self.togo=[]
		self.found=None
	
	# initialize search procedure
	# optionally, we can look specifically for the restypes in res[]. thus, if those restypes are not
	# found, the start point will be marked as not succesful, allowing us to find better places
	def startsearch(self, startnode, res=[]):
	
		print "  start bff search at ",startnode.location
	
		if len(self.togo)>0:
#			print "  still searching"
			return False
			

		# distance to point where the last search was started
		if self.start:
			if sum(map(abs, map(operator.sub, self.start.location, startnode.location))) < 3:
				for r in res:
					try:
						self.found[r]
						print "   refusing to start search: too close to last starting point, no new goals"
						return False
					except:
						pass
		
			
			
		self.found={}	
			
		if type(res)==int:
			res=[res]
		for r in res:
			self.found[r]=[]
	
		self.start=startnode
		self.togo=[startnode]
		self.known={startnode.lid:0}
	
		return True
		
		
	
	# perform search step	
	def update(self):
	
		if len(self.togo)>0:
			node=self.togo.pop(0)
			depth=self.known[node.lid]
		else:
#			print "  bff search terminated"
			return
						
		if depth>6:
			self.togo=[]
#			print "  bff search terminated due to range restr"
			return

		# something there?
		if node.resource and node.resource.amount>0:
			try:
				self.found[node.resource.type].append(node)
			except:
				self.found[node.resource.type]=[node]

		
		for nn in node.neighbours:
			try:
				self.known[nn.lid]
			except: # node nn is not known
				if nn.cost()<self.start.cost()*3:
					self.togo.append(nn)
				self.known[nn.lid]=depth+1
						


	
	# returns resources that have been found around position pos and fitting to resource set res
	# is being used by the mental map class to pass information about available resources to Need class
	def findings(self, res, pos):
		if not self.found:
			return None
		# only if not currently searching
		if not len(self.togo)>0:
			# if position is similar to where the search was started
			if self.start and sum(map(abs, map(operator.sub, self.start.location, pos))) < 3:
				# craft a list of node on which demanded resources are located
				results=[]
				for r in res:
					try:
						results.extend(self.found[r])
					except:
						pass
#				print "  returning resultset of length ", len(results)
				return results
				
			else:
				# if the resuls set is related to a distant start point, return null to indicate
				# that no search has been performed so far
				return None
		
		return []








# mental map of spots where breadth first searches were conducted and what were the results
class MentalMap():

	def __init__(self, mp):
	
		self.world = mp
	
		self.spots={}
		self.blanks={}
		
		self.bff=BFF()
		
		



	# indicator for BFF activities going on
	def waiting(self):
		return len(self.bff.togo)>0	
	
	
	# called in every frame by Needs instance, as long as "waiting"
	def update(self):
		self.bff.update()
		if len(self.bff.togo)<1:
			self.markspots()
	

	# the Needs class will request a list of surrounding resources via this method
	# all those that fit res, to be exact, and around the position pos
	def getResources(self, res, pos):
	
		# if we are not currently waiting for a bff search to terminate:
		if not self.waiting():
			# if there is a set of found resources waiting for us to pick it up
#			print " try to get a set of findings"
			findings = self.bff.findings(res, pos)

			if findings:
#				print " findings available"
				# pass it to personal Needs instance
				return findings
				
#			print " no findings available"
			return None
				
			# if there is no information about any found resources
#			else:
				# try to start a new search
#				self.bff.startsearch(self.world.getNode(pos), res)
			



	# rates start point of last search as search spots for all found resources
	def markspots(self):
	
		if self.bff.found:
	
			for r in rsc.usefulresources:
				try:
					self.markspot(r, self.bff.start, len(self.bff.found[r]))
				except:
					self.markspot(r, self.bff.start, 0)


			
	# avl = resource available yes or no
	def markspotOnScreen(self, res, pos, avl):
		pygame.draw.circle(self.world.gfx.layer, (100-100*avl,avl*100,0), (pos[0]*20+(res % 5)*4, pos[1]*20+(res/5)*4), 2)
		self.world.gfx.setDirty(self.world.getNode(pos))
	
	
	
	# remember a point pos on the map, where as many as nr instances of resource res have been 
	# spotted around. if nr is 0, pos is remembered as a blank to avoid looking here again
	def markspot(self, res, node, nr):
	
		pos=node.location
	
		if nr>0:
			if not node.water>0:
				# if there is a spot nearby which says that this resource isnt aroung, remove that
				try:
					nearestblank = self.blanks[res].nearest(pos)
					if nearestblank.dist(pos) < 4:
						nearestblank.remove()
				except:
					pass
				
			
				try:
					spots=self.spots[res]
					nearest = spots.nearest(pos)
					# knotenkonkurrenz
					if nearest.dist(pos) < 4:
						if nearest.data <= nr:
							spots.add(pos, nr)
							self.markspotOnScreen(res, pos, True)
							# wenn neuer spot besser ist, alten loeschen
							if nearest.data < nr:
								nearest.remove()
					# naehster spot weit genug weg
					else:
						spots.add(pos,nr)
						self.markspotOnScreen(res, pos, True)

				# kein kd-baum fuer res type
				except:
					spots=kd.tree()
					spots.add(pos, nr)
					self.spots[res]=spots
					self.markspotOnScreen(res, pos, True)
				
		# res type nicht aufzufinden		
		else:
			# if location has been remembered as a spot for this resource, remove if
			try:
				invalid = self.spots[res].lookup(pos)
				invalid.remove()
			except:
				pass
			# memorize this location as not suitable for searching this resource
#			print " mark pos", pos, " as dead spot for res ", res
			self.markspotOnScreen(res, pos, False)
			try:
				self.blanks[res].add(pos, nr)
			except:
				blanks=kd.tree()
				blanks.add(pos, nr)
				self.blanks[res]=blanks
				# TODO: statt nr=0 vielleicht nen zeitstempel um das updaten zu koennen?
				
			
						
			
	
	

		
	
	
	# suggests a point nearby which might be a better place to look for res type
	# since it is meant to be more distant to the res type dead spots
	def nextpos(self, res, pos):
	
		if len(self.spots)<1 and len(self.blanks)<1:
#			print " no memories whatsoever so far. aborting suggestion"
			return None
		
#		print " preparing next step..."
	
		best=None
		
		# get IDs of all nodes known from last bff search that have a minimum distance (depth) of 2
		nodes = map(lambda i:i[0], filter(lambda i:i[1]>3, self.bff.known.items()))
		
		if len(nodes)<1:
			nodes = map(lambda i:i[0], self.bff.known.items())
			
		if len(nodes)<1:
			return None
		
		for i in xrange(0,10):
		
			n = self.world.getNodeByID(rnd.choice(nodes))
				
			x,y=n.location
				
			try:
				nb = self.closestblank(res, (x,y))
				dist=sum(map(abs, map(operator.sub, nb, (x,y))))
				if n.water > 0:			
					dist/=4
				
			except:
#				print "no dead spots for res ", res
				dist=100
				
		
			if best is None:
				best = ((x,y),dist)
			else:
				if dist>best[1]:
					best=((x,y),dist)
				
#		print "suggesting destination ",best[0]
		return best[0]
			
		
	
	
	# returns the closest dead spot for a resource type
	def closestblank(self, res, pos):
	
		if type(res) == list:

			best=None
			
			for r in res:

				try:
					spot=self.blanks[r].nearest(pos)
					dist=spot.dist(pos)
					if best is None:
						best = (spot.pos, dist)
					else:
						if dist<best[1]:
							best=(spot.pos, dist)
				except:
					pass
				
			return best[0]
		
		else:
			try:
				return self.blanks[res].nearest(pos).pos
			except:
				return None


	# returns the closest spot for for a resource type
	def closestspot(self, res, pos):
	
		if type(res) == list:
			
			best=None
			
			for r in res:
			
				try:
					spot=self.spots[r].nearest(pos)
					dist=spot.dist(pos)
					if best is None:
						best = (spot.pos, dist)
					else:
						if dist<best[1]:
							best=(spot.pos, dist)
					
				except:
					pass

			try:
				return best[0]
			except:
				pass


		else:	
			try:
				return self.spots[res].nearest(pos).pos
			except:
				return None
			
		
	# returns the spot for this resource which probably has the most of them
	def bestspot(self, res):
	
		if type(res) == list:
		
			best=None
			
			for r in res:
			
				try:
					most=sorted(self.spots[r].toList(), key=lambda s:s[1]).pop()
					if best is None:
						best = most
					else:
						if most[1]>best[1]:
							best=most
				except:
					pass
					
				return best
	
		else:
			try:
				return sorted(self.spots[res].toList(), key=lambda s:s[1]).pop()
			except:
				return None
				
				
		
