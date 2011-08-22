import pygame
import os.path


grass=[]
water=[]
setup=False

def init():
	print "setting up imagery"
	global grass, water, setup

	setup=True

	#load grass images	
	level=0
	variant=0

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
		
		grass.append(variants)
		level+=1
		filename="data/grass%02d.png" % (level)
		
		
	#load water images
	water = []
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
		
		water.append(variants)
		level+=1
		filename="data/water%02d.png" % (level)			
		
		
		
		
		
def getImage(node):
	global grass, water, setup

	if not(setup):
		init()

	# water
	if node.water > 0:
		level=min(int(node.water),len(water)-1)
		variant = node.variant % len(water[level])
		image=water[level][variant].copy()
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
	
	level = min(int(node.vegetation-1),len(grass)-1)
	variant = node.variant % len(grass[level])

	return grass[level][variant]

