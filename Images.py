import pygame
import os.path

import Jaja


setup=False

grass=[]
water=[]

icons=[]

jajas=[]

ICON_MAP=0
ICON_BUBBLE=1


def init():
	print "setting up imagery"
	global grass, water, setup, icons

	setup=True

	#load grass images	
	level=0
	variant=0

	filename="data/grass%02d.png" % (level)
	while os.path.isfile(filename):
		variants=[]
		
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
	level=0
	variant=0
		
	filename="data/water%02d.png" % (level)
	while os.path.isfile(filename):
		variants=[]
		
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
		
	# load little icon imagery
	icons.append(pygame.image.load("data/map.png").convert_alpha())
	icons.append(pygame.image.load("data/bubble.png").convert_alpha())
	
	
	#load jaja sprites 
	sprite=pygame.image.load("data/jaja01.png").convert_alpha()
	jajas.append(sprite)
	sprite=pygame.image.load("data/jaja00.png").convert_alpha()
	jajas.append(sprite)
	
		
		
		
		
		
def getMapNodeImage(node):

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



def getIconImage(iconID):
	if not(setup):
		init()
	return icons[iconID]
	

def getJajaImage(jaja):
	if jaja.action is Jaja.Jaja.ACT_SLEEP:
		return jajas[0]
	if jaja.action in (Jaja.Jaja.ACT_WALK, Jaja.Jaja.ACT_STAND):
		return jajas[1]
	return None
	
	
