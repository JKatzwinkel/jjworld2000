import random as rnd
import KDTree as kd
import operator

# breadth first finder
class BFF(object):

	def __init__(self):
	
		self.start=None
		self.known={}
		self.togo=[]
		self.found={}
		
	
	# initialize search procedure
	# optionally, we can look specifically for the restypes in res[]. thus, if those restypes are not
	# found, the start point will be marked as not succesful, allowing us to find better places
	def search(self, startnode, res=[]):
	
		if self.searching():
			print "still searching"
			return	
			
		self.found={}	
			
		if type(res)==int:
			res=[res]
		for r in res:
			self.found[r]=[]
	
		self.start=startnode
		self.togo=[startnode]
		self.known={startnode.lid:0}
		
	
	# perform search step	
	def update(self):
	
		if len(self.togo)>0:
			node=self.togo.pop(0)
			depth=self.known[node.lid]
		else:
			return
			
		print depth, len(self.togo)
			
		if depth>6:
			self.togo=[]
			return
			
		
		for nn in node.neighbours:
			try:
				self.known[nn.lid]
			except: # node nn is not known
				if nn.cost()<self.start.cost()*3:
					self.togo.append(nn)
				self.known[nn.lid]=depth+1
				# something there?
				if nn.resource and nn.resource.amount>0:
					print "found resource ", nn.resource.type
					try:
						self.found[nn.resource.type].append(nn)
					except:
						self.found[nn.resource.type]=[nn]
						
	
	# still searchin? yes no		
	def searching(self):
		return len(self.togo)>0










# mental map of spots where breadth first searches were conducted and what were the results
class MentalMap(object):

	def __init__(self, realmap):
	
		self.realmap = realmap
	
		self.spots={}
		self.blanks={}
		
		self.bff=BFF()
		
	
	# remember a point pos on the map, where as many as nr instances of resource res have been 
	# spotted around. if nr is 0, pos is remembered as a blank to avoid looking here again
	def markspot(self, res, node, nr):
	
		pos=node.location
	
		if nr>0:
			if not node.water>0:
				try:
					spots=self.spots[res]
					nearest = spots.nearest(pos)
					# knotenkonkurrenz
					if nearest.dist(pos) < 4:
						if nearest.data <= nr:
							spots.add(pos, nr)
							print "mark pos ", pos, " as spot for res ", res, nr
							# wenn neuer spot besser ist, alten loeschen
							if nearest.data < nr:
								nearest.remove()
					# naehster spot weit genug weg
					else:
						print "mark pos ", pos, " as spot for res ", res, nr
						spots.add(pos,nr)

				# kein kd-baum fuer res type
				except:
					spots=kd.tree()
					spots.add(pos, nr)
					self.spots[res]=spots
					print "mark pos ", pos, " as spot for res ", res, nr
				
		# res type nicht aufzufinden		
		else:
			print "mark pos", pos, " as dead spot for res ", res
			try:
				self.blanks[res].add(pos, nr)
			except:
				blanks=kd.tree()
				blanks.add(pos, nr)
				self.blanks[res]=blanks
				# TODO: statt nr=0 vielleicht nen zeitstempel um das updaten zu koennen?
				
			
			
	# rates start point of last search as search spots for all found resources
	def markspots(self):
	
		if self.bff.searching():
			print "still searching"
			return
	
		for i in self.bff.found.items():
			print "res ",i[0],": x",len(i[1])
			self.markspot(i[0], self.bff.start, len(i[1]))
			
			
	
	# suggests a point nearby which might be a better place to look for res type
	# since it is meant to be more distant to the res type dead spots
	def nextpos(self, res, pos):
	
		print "preparing next step..."
	
		best=None
		
		nodes = map(lambda i:i[0], filter(lambda i:i[1]>2, self.bff.known.items()))
		
		if len(nodes)<1:
			nodes = map(lambda i:i[0], self.bff.known.items())
		
		for i in xrange(0,7):
		
			n = self.realmap.getNodeByID(rnd.choice(nodes))
				
				
			x,y=n.location
				
			
			try:
				nb = self.closestblank(res, (x,y))
				dist=sum(map(abs, map(operator.sub, nb, (x,y))))
			except:
				print "no dead spots for res ", res
				dist=100
				
		
			if best is None:
				best = ((x,y),dist)
			else:
				if dist>best[1]:
					best=((x,y),dist)
				
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
					
				return best[0]

		else:	
			try:
				return self.spots[res].nearest(pos).pos
			except:
				return None
			
