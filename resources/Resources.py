import pygame
import random

import Resource



class Pillow(Resource.Resource):

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 0, 1, mapnode)
		self.initImages()
		self.maxAmount=1
		

class Sterni(Resource.Resource):

	def __init__(self, amount, mapnode):
		
		Resource.Resource.__init__(self, 1, amount, mapnode)
		
		image=pygame.image.load("data/resource01.png").convert_alpha()
		
		# filling sterni images
		for i in range(0,19):
			self.images.append(None)
		self.images.append(image.copy())
			
		# randomly remove bottles from crate
		for i in range(18,0,-1):
			x=5+2*random.randrange(0,5)
			y=7+random.randrange(0,4)
			while image.get_at((x,y)).r < 100:
				x=5+2*random.randrange(0,5)
				y=7+random.randrange(0,4)
			image.set_at((x,y), pygame.Color(0,0,0,255))
			
			self.images[i]=image.copy()
		
		
		self.maxAmount=20
		
		
		
		
