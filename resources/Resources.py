import pygame
import random

import Resource
import Images



class Pillow(Resource.Resource):

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 0, 1, mapnode)
		self.initImages()
		self.maxAmount=1
		


class Sterni(Resource.Resource):

	def __init__(self, amount, mapnode):
		
		Resource.Resource.__init__(self, 1, amount, mapnode)
		
		image=Images.getResourceBaseImage(1).copy()
		
		self.images.append(image.copy())
			
		# randomly remove bottles from crate
		for i in range(0,20):
			x=5+2*random.randrange(0,5)
			y=7+random.randrange(0,4)
			while image.get_at((x,y)).r < 100:
				x=5+2*random.randrange(0,5)
				y=7+random.randrange(0,4)
			image.set_at((x,y), image.get_at((x+1,y)))
			
			self.images.insert(0,image.copy())
		
		self.maxAmount=20
		self.effectivity=.2
		
		

class Busch(Resource.Resource):

	def __init__(self, amount, mapnode):
	
		Resource.Resource.__init__(self, 2, amount, mapnode)
		
		image=pygame.Surface((20,20), pygame.SRCALPHA, 32)
		baseimage=Images.getResourceBaseImage(2).copy()
		
		x=random.randrange(0,baseimage.get_rect().width/20)
		
		image.blit(baseimage, pygame.Rect((0,0,20,20)), pygame.Rect((x*20,0,20,20)))
		
		self.images.append(image.copy())
		
		for i in range(0,20):
			x=2+random.randrange(0,17)
			y=3+random.randrange(0,13)
			col = image.get_at((x,y))
			while col.g>col.r*2 or col.a<255:
				x=2+random.randrange(0,17)
				y=3+random.randrange(0,13)
				col = image.get_at((x,y))
			image.set_at((x,y), pygame.Color(200,0,0,255))
			
			self.images.append(image.copy())
		
		self.maxAmount=20
		
	# grow some berries
	def grow(self):
		if self.amount < self.maxAmount:
			if random.random()*self.mapnode.fertility() > 2:
				self.amount+=1
