import pygame
import os.path

import Jaja


setup=False

grass=[]
water=[]
icons=[]
jajas=[]
resrs=[]


ICON_MAP=0
ICON_BUBBLE=1


def init():
	print "setting up imagery"
	global grass, water, setup, icons, resrs

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
	
	# load jaja sprites 
	sprite=pygame.image.load("data/jaja01.png").convert_alpha()
	jajas.append(sprite)
	sprite=pygame.image.load("data/jaja00.png").convert_alpha()
	jajas.append(sprite)
	
	# load resource base images. detailed handling is done by the resource implementation themselfs
	resnr=0
	filename="data/resource%02d.png" % resnr
	
	while os.path.isfile(filename):
	
		baseimg=pygame.image.load(filename).convert_alpha()
		
		resrs.append(baseimg)
		
		resnr+=1
		filename="data/resource%02d.png" % resnr
		
		




		
		


# returns image for a certain map node
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
				pygame.draw.line(image,(100,200,100),(0,0),(0,19))
		neighbour=node.map.getNode((node.location[0],node.location[1]-1))
		if neighbour:
			if not(neighbour in node.map.waternodes):
				pygame.draw.line(image,(100,200,100),(0,0),(19,0))
		return image
	
	# grass
	if node.vegetation < 1: 
		image=pygame.Surface((20,20))
		# TODO: maybe, grass images should be transparent, too, which would make ground image rendering more adjustable
		image.fill((216-node.fertility()*2,242,203))
		return image
	
	level = min(int(node.vegetation-1),len(grass)-1)
	variant = node.variant % len(grass[level])

	return grass[level][variant]


# return an image for a certain signal icon
def getIconImage(iconID):
	if not(setup):
		init()
	return icons[iconID]
	

# return image expressing the current state of a certain character
def getJajaImage(jaja):
	if jaja.action is Jaja.Jaja.ACT_SLEEP:
		return jajas[0]
	if jaja.action in (Jaja.Jaja.ACT_WALK, Jaja.Jaja.ACT_STAND):
		return jajas[1]
	return None


# returns basic imagery for specified resource	
def getResourceBaseImage(restype):
	if restype>=len(resrs):
		return None
	return resrs[restype]
	
