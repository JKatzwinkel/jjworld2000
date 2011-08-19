import pygame
import Sprites
from decimal import *
import copy

class GfxHandler:

	def __init__(self, mp, screen):
		self.screen = screen;
		self.sprites = Sprites.Sprites(self.screen)				
		self.map = mp
		self.map.gfxHandler=self
		self.topleft=(0,0)
		self.screensize=self.screen.get_size()

		w,h=self.screensize
		self.background = pygame.Surface((self.map.width*20, self.map.height*20))
		#self.background.fill((230,230,230))

		
		self.dirty=[]
		
		
		self.drawMap(self.background)
		self.screen.blit(self.background, (0,0)+self.screensize)
		
		
	def drawMap(self, surface):
	
		
#		print h,w, sx,sy
		
#		for y in range(max(0,sy), min(sy+h/20,self.map.height)):
#			for x in range(max(0,sx), min(sx+w/20, self.map.width)):
#				n=self.map.getNode((x,y))
				
#		print len(self.map.dirty)		
				
		w,h=self.screensize		
				
#		leftdirty = copy.deepcopy(self.map.dirty)
		
#		for lid in self.map.dirty:
#			n = self.map.getNodeByID(lid)
#			
#			x,y=self.locationOnScreen(n)
			
#			if not(y<-20-20 or y>=h+20):
#				if not(x<-20-20 or x>=w+20):
					#self.map.dirty.remove(lid)
#					sprite=self.sprites.getSprite(n)
#					if sprite:
#						surface.blit(self.sprites.getSprite(n), (x,y))#pygame.Rect(x,y,20,20))

		for n in self.map.nodes:
			x,y=n.location
			sprite=self.sprites.getSprite(n)
			if sprite:
				surface.blit(sprite, (x*20,y*20))
						
#		self.map.dirty=leftdirty
		
								
		
	def locationOnScreen(self, node):
		x,y=node.location
		sx,sy=self.topleft
		x=x*20-sx
		y=y*20-sy
		return (x,y)
		
		
	def clean(self):
		pass
		
		
	def setDirty(self, location):
		self.dirty.append(pygame.Rect(location,(20,20)))
		
	
	def moveRange(self, direction):
	
		sx,sy=self.topleft
		mx,my=direction
		w,h=self.screensize
		
		if sx+mx>=0 & sx+mx+w<self.map.width*20:
			if sy+my>=0 & sy+my+h<self.map.height*20:
				sx+=mx
				sy+=my
				self.background.blit(self.background, (-mx,-my))
				
				if mx<0:
					for i in range(0,-mx/20+2):
						for y in range(sy/20, (sy+h)/20):
							n=self.map.getNode((sx/20-1+i,y))
							if n: n.setDirty()
				elif mx>0:
					for i in range(0,mx/20+2):
						for y in range(sy/20, (sy+h)/20):
							n=self.map.getNode(((sx+w)/20+2-i,y))
							if n: n.setDirty()
				
				self.topleft=(sx, sy)
				
		
		
	def update(self, pointOfView):
	
#		self.map.draw(self.background)
#		self.map.draw(self.screen, True)
		#self.screen.scroll(-1,0)
		
		screenrect = pygame.Rect(self.topleft,self.screensize)
		
		for r in self.dirty:
			if screenrect.colliderect(r):
				self.screen.blit(self.background, r.move(-self.topleft[0], -self.topleft[1]), r)
				
		self.dirty=[]
				
		#self.drawMap(self.background)
		#self.screen.blit(self.background, (-20,-20))

		
#		self.screen.blit(self.drawMap(), (0,0))
		
