import pygame
import os.path

class Images:

	def __init__(self, screen):

		#load grass images	
		self.grass = []
		level=0
		variant=0
		
#		filename="data/grass%02d%02d.png" % (level,variant)
#		while os.path.isfile(filename):
#			variants=[]
#			while os.path.isfile(filename):
#
#				sprite = pygame.sprite.Sprite()
#				sprite.image = pygame.image.load(filename).convert()
#				variants.append(sprite)
#				
#				variant+=1
#				filename="data/grass%02d%02d.png" % (level,variant)
#				
#			self.grass.append(variants)
#			
#			variant=0
#			level+=1
#			filename="data/grass%02d%02d.png" % (level,variant)

		filename="data/grass%02d.png" % (level)
		while os.path.isfile(filename):
			variants=[]
			
			levelsprites=pygame.sprite.Sprite()
			levelsprites=pygame.image.load(filename).convert()
			
			x=0
			while x<levelsprites.get_rect().width:
				image=pygame.Surface((20,20))
				image.blit(levelsprites, pygame.Rect((0,0,20,20)), pygame.Rect((x,0,20,20)))
				variants.append(image)
				x+=20
			
			self.grass.append(variants)
			level+=1
			filename="data/grass%02d.png" % (level)
			
			
		#load water images
		self.water = []
		level=0
		variant=0

			
		filename="data/water%02d.png" % (level)
		while os.path.isfile(filename):
			variants=[]
			
			levelsprites=pygame.sprite.Sprite()
			levelsprites=pygame.image.load(filename).convert()
			
			x=0
			while x<levelsprites.get_rect().width:
				image=pygame.Surface((20,20))
				image.blit(levelsprites, pygame.Rect((0,0,20,20)), pygame.Rect((x,0,20,20)))
				variants.append(image)
				x+=20
			
			self.water.append(variants)
			level+=1
			filename="data/water%02d.png" % (level)			
			
			
			
			
			
	def getImage(self, node):
		# water
		if node.water > 0:
			level=min(int(node.water),len(self.water)-1)
			variant = node.variant % len(self.water[level])
			image=self.water[level][variant].copy()
			# line to mark shore
			neighbour=node.map.getNode((node.location[0]-1,node.location[1]))
			if neighbour:
				if not(neighbour in node.map.waternodes):
					pygame.draw.line(image,(100,100,100),(0,0),(0,19))
			neighbour=node.map.getNode((node.location[0],node.location[1]-1))
			if neighbour:
				if not(neighbour in node.map.waternodes):
					pygame.draw.line(image,(100,100,100),(0,0),(19,0))
			return image
		
		# grass
		if node.vegetation < 1: 
			image=pygame.Surface((20,20))
			image.fill((255,255,255))
			return image
		
		level = min(int(node.vegetation-1),len(self.grass)-1)
		variant = node.variant % len(self.grass[level])

		return self.grass[level][variant]

