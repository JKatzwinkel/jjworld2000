import pygame
import random
import math


class Jaja(pygame.sprite.Sprite):
	image=None
	
	
	def __init__(self, location, mp):
		pygame.sprite.Sprite.__init__(self)
		
		if not(Jaja.image):
			Jaja.image=pygame.image.load("data/jaja00.png").convert_alpha()
			
		self.image=Jaja.image
		
		self.map=mp
		
		self.location=location
		self.currentmapnode=self.map.getNode((int(round(self.location[0]+.5)),int(round(self.location[1]+.5))))
		self.path=[]
		
		
	def locationOnScreen(self):
		x,y=self.location
		sx,sy=self.map.gfx.topleft
		x=x*20-sx
		y=y*20-sy+int(self.currentmapnode.water>0)*2
		return (int(x),int(y))
		
	def draw(self, surface):
		if not(self.currentmapnode.water>0):
			surface.blit(self.image, self.locationOnScreen())
		else:
			x,y=self.locationOnScreen()
			surface.blit(self.image, (x,y), (0,0,20,13))
		
		
	def move(self):
		x,y=self.location
		nx,ny=self.currentmapnode.location
		
		# to be opt
		if x>nx+.5 or x<nx-.5 or y>ny+.5 or y<ny-.5:
			self.currentmapnode=self.map.getNode((int(round(self.location[0])), int(round(self.location[1]))))
		
		self.map.gfx.setDirty((int(x*20),int(y*20)),(20,25))
		
		if len(self.path)>0:
			#print len(self.path)
			
			dest=self.path[len(self.path)-1]
			dx,dy=dest.location
			
			mx=dx-x
			my=dy-y
			rad=math.hypot(mx,my)
			
			mx/=rad
			my/=rad
			
			speed=.1/(1+self.currentmapnode.vegetation+self.currentmapnode.water*10)
			
			if rad>.05:
				x+=mx*speed
				y+=my*speed
				self.location=(x,y)
			else:
				self.path.pop()
			
#		else:
#			x,y=self.location
#			self.path.append(self.map.getNode((x-1+random.randint(0,1)*2, y-1+random.randint(0,1)*2)))
