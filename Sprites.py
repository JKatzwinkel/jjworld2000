import pygame
import os.path

class Sprites:

	def __init__(self, screen):
	
		self.grass = []
		level=0
		variant=0
		
		filename="data/grass%02d%02d.png" % (level,variant)
		while os.path.isfile(filename):
			variants=[]
			while os.path.isfile(filename):

				sprite = pygame.sprite.Sprite()
				sprite.image = pygame.image.load(filename).convert()
				variants.append(sprite)
				
				variant+=1
				filename="data/grass%02d%02d.png" % (level,variant)
				
			self.grass.append(variants)
			
			variant=0
			level+=1
			filename="data/grass%02d%02d.png" % (level,variant)
			
			
			
	def getSprite(self, node):
		if node.vegetation < 1: return None
		
		level = min(int(node.vegetation-1),3)
		variant = node.variant % len(self.grass[level])

		return self.grass[level][variant].image

