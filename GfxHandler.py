import pygame
from decimal import *
import copy

import Images

class GfxHandler:

	def __init__(self, mp, screen):
		self.screen = screen;
		self.images = Images.Images(self.screen)				
		self.map = mp
		self.map.gfx=self
		self.topleft=(0,0)
		self.screensize=self.screen.get_size()

		w,h=self.screensize
		self.background = pygame.Surface((self.map.width*20, self.map.height*20))

		
		self.dirty=[]
		
		
		self.drawMap(self.background)
	#	self.screen.blit(self.background, (0,0)+self.screensize)
		
		
	# initializes background
	def drawMap(self, surface):
	
		w,h=self.screensize		

		for n in self.map.nodes:
			self.map.draw(n)
#			x,y=n.location
#			sprite=self.images.getImage(n)
#			if sprite:
#				surface.blit(sprite, (x*20,y*20))
						
		
								
		
	def locationOnScreen(self, node):
		x,y=node.location
		sx,sy=self.topleft
		x=x*20-sx
		y=y*20-sy
		return (x,y)
		
		
	def setDirty(self, location):
		self.dirty.append(pygame.Rect(location,(20,20)))				
		
		
	def update(self, pointOfView):
	
		sx,sy=self.topleft
		w,h=self.screensize
		
		mx=pointOfView[0]-sx
		my=pointOfView[1]-sy
		
		self.screen.scroll(-mx,-my)
		
		if mx>0:
			self.dirty.append(pygame.Rect((sx+w,sy),(mx,h)))
		if mx<0:
			self.dirty.append(pygame.Rect((sx+mx,sy),(mx,h)))
		if my>0:
			self.dirty.append(pygame.Rect((sx,sy+h),(w,my)))
		if my<0:
			self.dirty.append(pygame.Rect((sx,sy+my),(w,my)))
		
		self.topleft = pointOfView
		
		screenrect = pygame.Rect(self.topleft,self.screensize)
		
		for r in self.dirty:
			if screenrect.colliderect(r):
				self.screen.blit(self.background, r.move(-self.topleft[0], -self.topleft[1]), r)
				
		self.dirty=[]
				
		#self.drawMap(self.background)
		#self.screen.blit(self.background, (-20,-20))

		
#		self.screen.blit(self.drawMap(), (0,0))
		
