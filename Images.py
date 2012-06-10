import pygame
import os.path

import Jaja


setup=False

grass=[] #land vegetation images
water=[] #water images
lllis=[] #water lillies
icons=[] #sprites for versatile purposes
jajas=[] #jaja sprites
resrs=[] #sprites for collectable ressources


ICON_MAP=0
ICON_BUBBLE=1




def init():
	print "setting up imagery"
	global grass, water, setup, icons, resrs

	setup=True

	#load grass images	
	load("data/grass.png", grass)
			
			
	#load water images
	load("data/water00.png", water)	
		
		
	#load water lillie images
	load ("data/lillies.png", lllis)
		
			
		
	# load little icon imagery
	icons.append(pygame.image.load("data/map.png").convert_alpha())
	icons.append(pygame.image.load("data/bubble.png").convert_alpha())
	
	# load jaja sprites 
	sprite=pygame.image.load("data/jaja00.png").convert_alpha()
	jajas.append(sprite)
	sprite=pygame.image.load("data/jaja01.png").convert_alpha()
	jajas.append(sprite)
	sprite=pygame.transform.flip(pygame.image.load("data/jaja01.png").convert_alpha(), True, False)
	jajas.append(sprite)
	sprite=pygame.image.load("data/jaja02.png").convert_alpha()
	jajas.append(sprite)
	sprite=pygame.transform.flip(pygame.image.load("data/jaja02.png").convert_alpha(), True, False)
	jajas.append(sprite)
	
	# load resource base images. detailed handling is done by the resource implementation themselfs
	resnr=0
	filename="data/resource%02d.png" % resnr
	
	while os.path.isfile(filename):
	
		baseimg=pygame.image.load(filename).convert_alpha()
	#	print "loading image", filename
		
		resrs.append(baseimg)
		
		resnr+=1
		filename="data/resource%02d.png" % resnr
		
		



# loads a set of sprites into a two-dimensional list
# the set is expected in file filename, the list is expected to be [] when passed
# sprites are to be stored as a matrix of increasing amount (rows)
# and differing variants (column) of a specific resource
def load(filename, imglist):

	if os.path.isfile(filename):
		sprites=pygame.image.load(filename).convert_alpha()
		
		width=sprites.get_rect().width
		height=sprites.get_rect().height
		
		for level in range(0,width,20):
			variants=[]
		
			for variant in range(0,height,20):			
				image = pygame.Surface((20,20), pygame.SRCALPHA)
				image.blit(sprites, (0,0), pygame.Rect((level,variant,20,20)))
				variants.append(image)
				
			imglist.append(variants)


		
def erase(surface, pos):
	surface.fill((0,0,0,0), (pos, (20,20)))
		


# returns image for a certain map node
def getMapNodeImage(node):

	if not(setup):
		init()

	# water
	if node.water > 0:

		# wir schummeln hier uebelst und verwenden zur unterschiedlichen darstellung von wasser in
		# derselben auspraegung statt der variante die water-variable selbst. das machen wir wegen der seerosen (s.u.)
		# damit die bei wellengang nicht so wackeln
		level = int(node.water) % len(water)
		
		image=water[level][0].copy()
		# line to mark shore
		neighbour=node.map.getNode((node.location[0]-1,node.location[1]))
		if neighbour:
			if not(neighbour in node.map.waternodes):
				pygame.draw.line(image,(100,200,100),(0,0),(0,19))
		neighbour=node.map.getNode((node.location[0],node.location[1]-1))
		if neighbour:
			if not(neighbour in node.map.waternodes):
				pygame.draw.line(image,(100,200,100),(0,0),(19,0))
			
		# water lillies <3
		if node.vegetation>=3:
			level = min(int(node.vegetation-3),len(lllis)-1)
			variant = node.variant % len(lllis[level])				
			image.blit(lllis[level][variant], (0,0))
				
		return image
	
	# grass
	if node.vegetation < 1: 
		image=pygame.Surface((20,20))
		# TODO: maybe, grass images should be transparent, too, which would make ground image rendering more adjustable
		if node.vegetation < 0:
			image.fill((206,220,160))
		else:
			image.fill((206,242,203))
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
	if jaja.action is Jaja.ACT_SLEEP:
		return jajas[0]
	if jaja.action in (Jaja.ACT_WALK, Jaja.ACT_STAND):
		return jajas[jaja.direction]
	if jaja.action is Jaja.ACT_CONSUME:
		return jajas[2+jaja.direction]
	return None


# returns basic imagery for specified resource	
def getResourceBaseImage(restype):
	if restype>=len(resrs):
		return None
	return resrs[restype]
	
	
	
# renders the whole world and saves the image to disk
def screenshot(characters, gfx):

	bckgrnd=gfx.satellite()
	
	for c in characters:
		c.draw(bckgrnd, False)
	
	i = 0
	filename="screenshots/world%03d.png" % i
	while os.path.isfile(filename):
		i+=1
		filename="screenshots/world%03d.png" % i
	
	pygame.image.save(bckgrnd, filename)
	print "screenshot of world saved under ", filename

