import pygame
import Sprites
from decimal import *

class GfxHandler:

	def __init__(self, mp, screen):
		self.screen = screen;
		self.background = None
		self.sprites = Sprites.Sprites(self.screen)				
		self.map = mp
		self.topleft=(0,0)
		self.screensize=self.screen.get_size()
		self.dirty = []
		
		
	def drawMap(self):
	
		result=pygame.Surface(self.screensize)
		result.fill((255,255,255))
		
		sx,sy=self.topleft
		w,h=self.screensize
#		print h,w, sx,sy
		
		for y in range(max(0,sy), min(sy+h/20,self.map.height)):
			for x in range(max(0,sx), min(sx+w/20, self.map.width)):
#				print x,y
				n=self.map.getNode((x,y))
				
				sprite=self.sprites.getSprite(n)
				if sprite:
					result.blit(self.sprites.getSprite(n), pygame.Rect((x-sx)*20,(y-sy)*20,20,20))
								
		return result
		
	def clean(self):
		pass
		
	
	def moveRange(self, direction):
	
		sx,sy=self.topleft
		mx,my=direction
		w,h=self.screensize
		
		if sx+mx>=0 & sx+mx+w/20<self.map.width:
			if sy+my>=0 & sy+my+h/20<self.map.height:
				self.topleft=(sx+mx, sy+my)
		
		
	def update(self):
		self.screen.blit(self.drawMap(), (0,0))
		
