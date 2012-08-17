import operator
import os.path
import pygame

import Images
import Needs



effectivities={}

def register(restype, function, amount):
	effectivities[(restype, function)]=amount
	Needs.register(restype, function)


class Resource:

	def __init__(self, restype, amount, mapnode):
		
		self.type=restype
		self.amount=amount
		self.maxAmount=amount
		self.mapnode=mapnode
		self.images=[]
		self.effects={}
		
		# load effects from registry
		for e in effectivities.items():
			if e[0][0] is restype:
				self.effects[e[0][1]]=e[1]
		
#		print "create resource ",restype,"at ", mapnode.location
		
	
	# must be called by constructor of inheriting class, unless the inheriting class choses to fill
	# its images[] array itself. to do this, it can call Images.getResourceBaseImageCopy(restype).
	#
	# gets a resource level image set as retrieved from disk. stores that set in one-dimensional array
	# when resource artwork holds more than one set of level images (thus, more than one variant), 
	# an arbitrary set variant is chosen.
	# and understands it as list of sprites representing the resource in increasing amount
	#
	def initImages(self):
		
		ressprites=Images.getResourceBaseImageCopy(self.type)
		
		self.images=[]
	
		x=0
		while x<ressprites.get_rect().width:
			#print "add resoruce imagery", x
			image=pygame.Surface((20,20), pygame.SRCALPHA, 32)
			image.blit(ressprites, pygame.Rect((0,0,20,20)), pygame.Rect((x,0,20,20)))
			self.images.append(image)
			x+=20


	# returns true as long as there is sth to consume
	# and, of course, decreases the amount of this resource
	def consume(self, needs):
	
		if self.amount > 0:
			self.amount-=1
			self.draw(self.mapnode.map.gfx.layer)
			
			for effect in self.effects.items():
				effect[0](needs, effect[1])
			
			needs.consume()
			return True
		else:
			return False
			
	
	# draws the resource's image on the surface (absolute coordinates)
	def draw(self, surface):
		
		if self.amount>0:
			index= 1 + (len(self.images)-1) * self.amount / self.maxAmount - 1 
		else:
			index=0
		
		image=self.images[index]
		
		#print "drawing image nr. ", index
		
		pos=map(operator.mul, self.mapnode.location, (20,20))
		
		Images.erase(surface, pos)
		surface.blit(image, pos)
		
		self.mapnode.map.gfx.setDirty(self.mapnode)
		
		
	# to be implemented by inheriting class
	def grow(self):
		pass
		
		

