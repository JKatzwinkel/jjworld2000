import pygame
from pygame.locals import *
import Images
import Map
import MentalMap
import GfxHandler


pygame.init()
screen=pygame.display.set_mode((1000,700),HWSURFACE)
Images.init()

m=Map.Map(50,35)
m.initDetails()

m.gfx.update((0,0))
pygame.display.flip()

mm=MentalMap.MentalMap(m)


pos=(0,0)
	

# mark current position on map
def step():

	global screen
	
	print pos
	pygame.draw.circle(screen, (100,70,0), (pos[0]*20+10,pos[1]*20+10), 10)
		
	m.gfx.update((0,0))
	pygame.display.flip()
	
	
# mark arbitrary position on map
def show(pos):

	global screen
	
	pygame.draw.circle(screen, (100,50,60), (pos[0]*20+10,pos[1]*20+10), 10)
	m.gfx.update((0,0))
	pygame.display.flip()
	

# (only give one res type)
def search(res):

	global pos, screen

	print pos
	mm.bff.search(m.getNode(pos), [res])
	
	while mm.bff.searching():
		mm.bff.update()
		
	mm.markspots()
	
	if len(mm.bff.found[res])<1:
		pygame.draw.circle(screen, (200,0,0), (pos[0]*20+10, pos[1]*20+10), 5)
	else:
		pygame.draw.circle(screen, (100,200,0), (pos[0]*20+10, pos[1]*20+10), 5)
		
	pos=mm.nextpos(res, pos)
	pygame.draw.circle(screen, (100,100,200), (pos[0]*20+10, pos[1]*20+10), 4)
		
	m.gfx.update((0,0))
	pygame.display.flip()
	

# show all nodes of last bff search
def area():
	global screen
	
	for vst in mm.bff.known.items():
		x,y = m.getNodeByID(vst[0]).location
		dpt = vst[1]
		pygame.draw.circle(screen, (150+dpt*10,150,240-dpt*20), (x*20+10, y*20+10), 2)
	
	m.gfx.update((0,0))
	pygame.display.flip()
	

# give closest spot for res
def spot(res):
	
	return mm.closestspot(res, pos)


