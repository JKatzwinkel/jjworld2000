import pygame
from pygame.locals import *
import Images
import Map
import MentalMap
import GfxHandler

import random as rnd


pygame.init()
screen=pygame.display.set_mode((1000,700),HWSURFACE)
Images.init()

m=Map.Map(50,35)
m.initDetails()

for i in range(0,10):
	node=rnd.choice(m.nodes)
	if not node.water>0:
		node.spawnResource(1,20)

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
	


def search(res):

	global pos, screen
	
	if type(res)==int:
		res=[res]

	print pos
	mm.bff.startsearch(m.getNode(pos), res)
	
	while mm.bff.searching():
		mm.bff.update()
		
	mm.markspots()
	
	if reduce(lambda x,y: x and y, map(lambda r: len(mm.bff.found[r])<1, res)):
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
		pygame.draw.circle(screen, (min(255,150+int(dpt*10)),150,max(0,240-int(dpt*20))), (x*20+10, y*20+10), 2)
	
	m.gfx.update((0,0))
	pygame.display.flip()
	

# give closest spot for res
def spot(res):
	
	return mm.closestspot(res, pos)


