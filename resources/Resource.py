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

	
	# draws the resource's image on the surface (absolute coordinates)
	def draw(self, surface):
		
		image=self.images[len(self.images) * self.amount / self.maxAmount - 1 ]
		
		surface.blit(image, map(operator.mul, self.mapnode.location, (20,20)))
		

