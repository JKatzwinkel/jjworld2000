import operator
import os.path
import pygame

import Images


class Resource:

	def __init__(self, restype, amount, mapnode):
		
		self.type=restype
		self.amount=amount
		self.maxAmount=amount
		self.mapnode=mapnode
		self.images=[]
		
		print "create resource ",restype,"at ", mapnode.location
		
	
	
	# looks for a file fitting this resource type in the data directory
	def initImages(self):
		
		filename="data/resource%02d.png" % self.type
		
		if os.path.isfile(filename):
		
			self.images=[]
		
			ressprites=pygame.image.load(filename).convert_alpha()
		
			x=0
			while x<ressprites.get_rect().width:
				image=pygame.Surface((20,20), pygame.SRCALPHA, 32)
				image.blit(ressprites, pygame.Rect((0,0,20,20)), pygame.Rect((x,0,20,20)))
				self.images.append(image)
				x+=20


	# returns true as long as there is sth to consume
	# and, of course, decreases the amount of this resource
	def consume(self):
	
		if self.amount > 0:
			self.amount-=1
			return True
		else:
			return False
			
	
	# draws the resource's image on the surface (absolute coordinates)
	def draw(self, surface):
		
		index=len(self.images) * self.amount / self.maxAmount - 1 
		image=self.images[index]
		
		print "drawing image nr. ", index
		
		surface.blit(image, map(operator.mul, self.mapnode.location, (20,20)))
		
		self.mapnode.map.gfx.setDirty(self.mapnode)
		

