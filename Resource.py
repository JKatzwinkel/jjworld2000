import operator

import Images


class Resource:

	maximumAmounts=[0,		# nothing
					20]		# sterni

	def __init__(self, restype, amount, mapnode):
		
		self.restype=restype
		self.amount=amount
		self.mapnode=mapnode
		
		print "create resource ",restype,"at ", mapnode.location
		
	
	# draws the resource's image on the surface (absolute coordinates)
	def draw(self, surface):
		
		surface.blit(Images.getResourceImage(self), map(operator.mul, self.mapnode.location, (20,20)))
		

