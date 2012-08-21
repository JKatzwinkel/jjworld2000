import pygame
import random

import Resource
import Images
import Needs



class Pillow(Resource.Resource):

	Resource.register(0, Needs.recreate, .5)

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 0, mapnode, 1)
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

	def __init__(self, mapnode, amount):
		
		Resource.Resource.__init__(self, 1, mapnode, amount)
		
		image=Images.getResourceBaseImageCopy(1)
		
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
		
	def __init__(self, mapnode, amount):
	
		Resource.Resource.__init__(self, 2, mapnode, amount)
		
		image=Images.getResourceBaseImageCopy(2)
		
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
	
		Resource.Resource.__init__(self, 3, mapnode, 1)
		self.maxAmount=1		
		self.initImages()
	
	
	def consume(self, needs):
		Resource.Resource.consume(self, needs)
		self.amount=1
		
		
		
class Blumenkohl(Resource.Resource):

	Resource.register(4, Needs.eat, .4)
	
	def __init__(self, mapnode, amount):
	
		Resource.Resource.__init__(self, 4, mapnode, 1)
		self.maxAmount=1
		self.initImages()

	def grow(self):
		if self.amount < self.maxAmount:
			if random.random()*10<self.mapnode.fertility():
				self.amount+=1
		
		
class Pizza(Resource.Resource):
	
	Resource.register(5, Needs.eat, .7)
	
	def __init__(self, mapnode, amount):
	
		Resource.Resource.__init__(self, 5, mapnode, amount)
		self.maxAmount=8
		
		# get fresh round pizza
		image=Images.getResourceBaseImageCopy(5)
		self.images=[image.copy()]
		
		# initialize slice cutting functions
		# for cutting a slice, we erase the corresponding pixels by starting on top and erasing
		# row after row
		# 	 y start position	x start position	x range
		f=[	(-10, 				lambda i:0, 		lambda i:10-i),
			(-10,				lambda i:10-i,		lambda i:i),
			(0,					lambda i:i,			lambda i:10-i),
			(0,					lambda i:0,			lambda i:i),
			(0,					lambda i:-i,		lambda i:i),
			(0,					lambda i:-10,		lambda i:10-i),
			(-10,				lambda i:-10,		lambda i:i),
			(-10, 				lambda i:i-10, 		lambda i:10-i) ]
		
		transparent=pygame.Color(0,0,0,0)
		
		erased=[]
		
		for s in range(0,8):
			si=random.randrange(0,8)
			while si in erased:
				si=random.randrange(0,8)
			erased.append(si)
			# get the function that will control cutting the next slice
			fs=f[si]
			for i in range(0,10):
				sx=10+fs[1](i)
				for x in range(sx, sx+fs[2](i)):
					if random.randint(0,30)<30:
						image.set_at((x,10+fs[0]+i), transparent )
			self.images.append(image.copy())
			
		self.images.reverse()
	
		

class Rock(Resource.Resource):

	def __init__(self, mapnode):
		
		Resource.Resource.__init__(self, 6, mapnode, 1)
		self.maxAmount=1
		self.initImages()
		


class Pumpkin(Resource.Resource):

	Resource.register(7, Needs.eat, .5)

	def __init__(self, mapnode, amount):
			
		Resource.Resource.__init__(self, 7, mapnode, amount)
		self.maxAmount=2
		self.initImages()
		
	def grow(self):
		if self.amount < self.maxAmount:
			if random.random()*self.mapnode.fertility() > 1:
				self.amount+=1
			if random.random()>.95:
				self.mapnode.resource=None

