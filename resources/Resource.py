import operator

import Images


class Resource:

	def __init__(self, restype, amount, mapnode):
		
		self.type=restype
		self.amount=amount
		self.mapnode=mapnode
		self.images=[]
		
		print "create resource ",restype,"at ", mapnode.location
		
	
	# draws the resource's image on the surface (absolute coordinates)
	def draw(self, surface):
		
		surface.blit(Images.getResourceImage(self), map(operator.mul, self.mapnode.location, (20,20)))
		

