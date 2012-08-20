import pygame
from decimal import *
import copy
import operator

import Images
import Jajaworld




class GfxHandler:

	def __init__(self, width, height):
		self.topleft=(0,0)
		self.screensize=Jajaworld.screen.get_size()

		w,h=self.screensize
		self.background = pygame.Surface((width, height))
		self.layer	=	pygame.Surface((width, height), pygame.SRCALPHA, 32)

		self.dirty=[]
		
	
		
	# initializes background
	def drawMap(self, mp):
	
		print " draw world map"

		for n in mp.nodes:
			n.draw(self.background)
			self.setDirty(pygame.Rect(tuple(map(operator.mul, n.location, (20,20)))+(20,20)))
			if n.resource:
				n.resource.draw(self.layer)
						
		
								
	# returns the location of the given node relative to the current point of view
	def locationOnScreen(self, node):
		x,y=node.location
		sx,sy=self.topleft
		x=x*20-sx
		y=y*20-sy
		return (x,y)
		
		
	# marks a certain rectangle as to be redrawn
	# coordinates must be absolute and as in: (x, y, w, h)
	# can also mark a specified map node!!!
	def setDirty(self, area):
		if area.__class__.__name__ is 'Node':
			self.dirty.append(pygame.Rect(tuple(map(operator.mul, area.location, (20,20)))+(20,20)))
		else:
			self.dirty.append(area)				
		
		
	
	# updates the part of the world which can be displayed on the screen.
	# scrolling is handled here
	# cleaning of dirty rects, too
	def update(self, pointOfView):
	
		sx,sy=self.topleft
		w,h=self.screensize
		
		mx=pointOfView[0]-sx
		my=pointOfView[1]-sy
		
		Jajaworld.screen.scroll(-mx,-my)
		
		if mx>0:
			self.dirty.append(pygame.Rect((sx+w,sy+my),(mx,h)))
		if mx<0:
			self.dirty.append(pygame.Rect((sx+mx,sy+my),(-mx,h)))
		if my>0:
			self.dirty.append(pygame.Rect((sx+mx,sy+h),(w,my)))
		if my<0:
			self.dirty.append(pygame.Rect((sx+mx,sy+my),(w,-my)))
		
		self.topleft = pointOfView
		
		screenrect = pygame.Rect(self.topleft,self.screensize)
		
		for r in self.dirty:
			if screenrect.colliderect(r):
				Jajaworld.screen.blit(self.background, r.move(-self.topleft[0], -self.topleft[1]), r)
				Jajaworld.screen.blit(self.layer, r.move(-self.topleft[0], -self.topleft[1]), r)
				
		self.dirty=[]
		
		
	
	# renders the entire world
	def satellite(self):
	
		wrld = self.background.copy()
		wrld.blit(self.layer, (0,0))				
		
		return wrld
		
