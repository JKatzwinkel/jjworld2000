import pygame
import random

import Resource
import Images
import Needs



class Pillow(Resource.Resource):

	Resource.register(0, Needs.recreate, 0)

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 0, 1, mapnode)
		self.maxAmount=1
		self.initImages()
		
	def consume(self, needs):
		
		Resource.Resource.consume(self, needs)
		self.amount=1
		needs.sleep()
		


class Sterni(Resource.Resource):

	Resource.register(1, Needs.drink, .2)
	Resource.register(1, Needs.eat, .1)
	Resource.register(1, Needs.recreate, .1)

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
		
		

class Busch(Resource.Resource):

	Resource.register(2, Needs.eat, .2)
	Resource.register(2, Needs.drink, .1)
		
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
			if random.random()*self.mapnode.fertility() > 1:
				self.amount+=1


				
class Hahn(Resource.Resource):

	Resource.register(3, Needs.drink, .7)

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 3, 1, mapnode)
		self.maxAmount=1		
		self.initImages()
	
	
	def consume(self, needs):
		Resource.Resource.consume(self, needs)
		self.amount=1
		
		
		
class Blumenkohl(Resource.Resource):

	Resource.register(4, Needs.eat, .5)
	
	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 4, 1, mapnode)
		self.maxAmount=1
		self.initImages()

	def grow(self):
		if self.amount < self.maxAmount:
			if random.random()*10<self.mapnode.fertility():
				self.amount+=1
		
		
