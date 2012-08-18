#!/usr/bin/python
# coding: utf8

import operator
import math
from collections import deque

class Node(object):

	# constructor
	# pos mußt be tupel with at least 2 coordinates
	def __init__(self, pos=None, data=None, left=None, right=None, axis=0):
	
		self.pos=pos
		self.data=data
		self.axis=axis
		
		if not self.pos is None:
			self.left = Node(axis=(axis+1)%2)
			self.right = Node(axis=(axis+1)%2)
		else:
			self.left=None
			self.right=None
		
		
	# add node
	def add(self, pos, data):
	
		if self.pos is None:
			
			self.pos=pos
			self.data=data
			self.left=Node(axis=(self.axis+1)%2)
			self.right=Node(axis=(self.axis+1)%2)
			
		else:
		
			if pos[self.axis] < self.pos[self.axis]:
			
				self.left.add(pos,data)
				
			else:
			
				if pos == self.pos:
					self.data=data
	
				else:		
					self.right.add(pos, data)
		
					
	# add list of nodes
	# TODO: in ner rekursion liste übergeben? ist das schlau???
	def addlist(self, nodes, axis=0):
		
		if len(nodes)<1: return
		
		nodes.sort(key = lambda node : node.pos[axis])
		
		median=len(nodes) // 2
		
		piv = nodes[median]
		self.add(piv.pos,piv.data)
		
		self.left.addlist(nodes[:median], axis=(axis+1)%2)
		self.right.addlist(nodes[median+1:], axis=(axis+1)%2)
		
								
	# returns generator for a list of sorted nodes
	def inorder(self):

		if self.left:	
			if self.left.pos:
				for x in self.left.inorder():
					yield x
				
		yield self

		if self.right:		
			if self.right.pos:
				for x in self.right.inorder():
					yield x
				
				
	# returns height of tree
	def height(self, level=0):
	
		if not self.pos: 
			return level
	
		return max(self.left.height(level=level+1) , \
				 self.right.height(level=level+1))
	
	
	# returns the overall count of non-empty nodes
	@property
	def size(self):
		
		if self.pos is None:
			return 0
			
		return self.left.size+1+self.right.size
	
	
	# override toString()
	def __repr__(self):
		
		result=[]
		for x in self.inorder():
			if x.pos is not None:
				result.append((x.pos, x.data))
				
		return repr(result)
		
	
	# return as list
	def toList(self):
		return [ 
			(x.pos, x.data) 
			for x in 
			filter(lambda i:i.pos, self.inorder()) 
			]
		
			
		
			
	# returns the content of the node @ pos
	def lookup(self, pos):
	
		if self.pos is None:
			return None			
	
		if self.pos==pos:
			return self
	
		if pos[self.axis]<=self.pos[self.axis]:
			return self.left.lookup(pos)
			
		return self.right.lookup(pos)
		
		
	# returns manchester distance to a certain position
	def dist(self, pos):
	
		return sum(map(abs, map(operator.sub, self.pos, pos)))
		

	# return the node closest to given point
	def nearest(self, pos, best=None):
	
		if self.pos is None:
			return best
	
		if best is None:
			best=self
			
		if self.dist(pos) < best.dist(pos):
			best=self
			
		if pos[self.axis]<self.pos[self.axis]:
		
			best = self.left.nearest(pos, best)
			# check if we have to follow recursion of the other side
			if self.dist_from_axis(pos) < best.dist(pos):
				best = self.right.nearest(pos, best)
		
		else:
		
			best = self.right.nearest(pos, best)
			if self.dist_from_axis(pos) < best.dist(pos):
				best = self.left.nearest(pos, best)
			
		return best
			
		
	# returns how far this point is away from the axis this node is splitting
	def dist_from_axis(self, point):
		
		return abs(point[self.axis] - self.pos[self.axis])
		
			
	# löscht knoten, oder sucht knoten in unterbaum und löscht den, wenn pos übergeben wird
	def remove(self, pos=None):
		
		if type(pos) is tuple:
			rem=self.lookup(pos)
			if rem:
				rem.remove()
			return
		
		#TODO: soll ein knoten gelöscht werden, wird ein geeigneter ersatz unter seinen kindern gesucht.
		# geeignet ist der knoten mit dem minimalen wert auf der achse, welcher der zu löschende knoten teilt.
		# mit dessen inhalt wird der inhalt des zu löschenden knotens überschrieben. der ersatz wird zunächst in
		# der rechten achse gesucht, wenn es keine rechte achse gibt, in der linken.
		# der ersatz wird dann nach demselben verfahren gelöscht.
		# www.cs.umd.edu/class/spring2002/cmsc420-0401/pbasic.pdf
		
		if self.isleaf:
			self.data=None
			self.pos=None
			self.left=None
			self.right=None
			return
			
		if not self.right.pos is None:
			substitute=self.right.minimum(axis=self.axis)
		else:
			substitute = self.left.maximum(axis=self.axis)
			
#		print "substitute for ",self.pos," is ", substitute.pos
			
		self.pos = substitute.pos
		self.data= substitute.data
		
		substitute.remove()
		
		
		
	@property
	def isleaf(self):
	
		if self.left.pos is None:
			if self.right.pos is None:
#				print self.pos, " is leaf"
				return True
		
#		print self.pos, " is inner node"
		
		return False
		
		
	# gibt den knoten im unterbaum zurück, der nach der gegebenen achse am weitesten links ist
	def minimum(self, axis, best=None):
	
		if self.pos is None:
			return best
	
		if best is None:
			best = self
		elif self.pos[axis] <= best.pos[axis]:
			best = self
				
			
		if self.axis is axis:
			return self.left.minimum(axis, best)
			
		else:
			left = self.left.minimum(axis, best)
			right=self.right.minimum(axis, best)
			
			if left.pos[axis] <= right.pos[axis]:
				return left
			else:
				return right
			
			
	# gibt den knoten im unterbaum zurück, der nach der gegebenen achse am weitesten rechts ist
	def maximum(self, axis, best=None):
	
		if self.pos is None:
			return best
	
		if best is None:
			best = self
		elif self.pos[axis] >= best.pos[axis]:
			best = self
				
			
		if self.axis is axis:
			return self.left.maximum(axis, best)
			
		else:
			left = self.left.maximum(axis, best)
			right=self.right.maximum(axis, best)
			
			if left.pos[axis] >= right.pos[axis]:
				return left
			else:
				return right
			
# tree factory	
def tree():

	return Node()
	
	
# returns a balanced version of that tree
def balanced(tree):

	nodes=[]
	for x in tree.inorder():
		nodes.append(x)
		
	tree=Node()
	tree.addlist(nodes)
	return tree

	
def random():

	tree=Node()
	
	from random import randint as rnd
	
	for i in xrange(0,10):
		tree.add((rnd(0,10),rnd(0,10)),rnd(0,10))
		
	return tree
	
	
def delroot(tree):
	tree.remove()
	

# baumknoten in level order: wurzel, links, rechts, linkslinks, linksrechts, rechtslinks...
def levelorder(tree):

	depth=0
	height=tree.height
	nodes=deque()
	
	nodes.append(tree)
	while nodes and depth<height:
		node = nodes.popleft()
		
		yield node
		
		# mit __class__() wird so ne art Node-object erzeugt, das natuerlich voellig
		# leer ist, das aber wiederum ein .left-feld hat (und einen __class__()-konstruktor). deshalb geht das!
		
		nodes.append(node.left or node.__class__())
		nodes.append(node.right or node.__class__())
		
		if node.left or node.right:
			depth+=1
		


# TODO: abgeschrieben, muß nachvollzogen werden
def visualize(tree, max_level=100, node_width=10, left_padding=5):
    """ Prints the tree to stdout """

    height = min(max_level, tree.height()-1)
    max_width = pow(2, height)

    per_level = 1
    in_level  = 0
    level     = 0

    for node in levelorder(tree):

        if in_level == 0:
            print
            print
            print ' '*left_padding,

        width = int(max_width*node_width/per_level)

        node_str = (str(node.pos) if node.pos else '').center(width)
        print node_str,

        in_level += 1

        if in_level == per_level:
            in_level   = 0
            per_level *= 2
            level     += 1

        if level > height:
            break

    print
    print

	
	
if __name__=='__main__':
	
	tree=tree()
	
	from random import randint as rnd
	
	for i in xrange(0,100000):
		tree.add((rnd(0,100000),rnd(0,100000)),rnd(0,100000))
		
	print "not balanced: ",tree.height(), tree.size()
	tree= balanced(tree)
	print "balanced: ",tree.height(), tree.size()
	
