import KDTree as kd
import random as rnd

	

class Spots(object):

	def __init__(self):
	
		self.map=[]
		for x in range(0,20):
			row=[]
			for y in range(0,20):
				if rnd.randint(0,20)<1:
					row.append(rnd.randint(1,3))
				else:
					row.append(0)
			self.map.append(row)
				
		
		self.spots = {}
		self.blanks= {}
		
	
	def savespot(self, res, pos):
	
		nr=0
		for x in range(max(0,pos[0]-3), min(19,pos[0]+3)):
			for y in range(max(0,pos[1]-3), min(19,pos[1]+3)):
				if abs(pos[0]-x)+abs(pos[1]-y)<4:
					if self.map[y][x] is res:
						nr+=1
						
		print " found ",nr,"sources for type ",res," around pos. ",pos
					
	
		if nr > 0:
			self.map[pos[1]][pos[0]]="s"
			try:
				self.spots[res].add(pos, nr)
			except:
				self.spots[res]=kd.tree()
				self.spots[res].add(pos, nr)
		else:
			self.map[pos[1]][pos[0]]="b"
			try:
				self.blanks[res].add(pos, nr)
			except:
				self.blanks[res]=kd.tree()
				self.blanks[res].add(pos, nr)
				
	
	def nearestspot(self, res, pos):
		
		try:
			return self.spots[res].nearest(pos)
		except:
			print "no spots for type ",res," known"
			

	def nearestblank(self, res, pos):
		
		try:
			return self.blanks[res].nearest(pos)
		except:
			print "no blanks for type ",res," known"
			
	
	def drawmap(self):
		
		for y in range(0,20):
			row=self.map[y]
			for x in range(0,20):
			
				if row[x] in ("s", "b"):
					print row[x]," ",
				elif row[x]>0:
					print row[x]," ",
				else:
					print "  ",
			print ""				
			
		
	def nextsearchpoint(self, res, pos):
	
		best=None
		for i in range(0,5):
			x=min(19,max(0,pos[0]-3+rnd.randint(0,6)))
			y=min(19,max(0,pos[1]-3+rnd.randint(0,6)))
			
			nb=self.nearestblank(res, (x,y)).pos
			dist=abs(nb[0]-x)+abs(nb[1]-y)
			
			if best is None:
				best=((x,y),dist)
			else:
				if best[1]<dist:
					best=((x,y),dist)
		
		print "best point to continue search: ",best
		return best[0]
		

s=Spots()
s.drawmap()
s.savespot(1,(5,0))
s.drawmap()


