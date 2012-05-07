#!/usr/bin/python
# coding: utf8

import operator

class Node(object):

	# constructor
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
	def addlist(self, nodes, axis=0):
		
		if len(nodes)<1: return
		
		nodes.sort(key=lambda node:node[0][axis])
		
		median=len(nodes) // 2
		
		piv = nodes[median]
		self.add(piv[0], piv[1])
		
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
	def size(self):
		
		if self.pos is None:
			return 0
			
		return self.left.size()+1+self.right.size()
	
	
	# override toString()
	def __repr__(self):
		
		result=[]
		for x in self.inorder():
			if x.pos is not None:
				result.append((x.pos, x.data))
				
		return repr(result)
			
		
			
	# returns the content of the node @ pos
	def lookup(self, pos):
	
		if self.pos is None:
			return None
	
		if pos[self.axis]<self.pos[self.axis]:
			return self.left.lookup(pos)
			
		elif pos[self.axis]>self.pos[self.axis]:
			return self.right.lookup(pos)
			
		else:
			return self.data
			
		
	# returns euclidian distance to a certain position
	def dist(self, pos):
	
		return sum(map(abs, map(operator.sub, self.pos, pos)))
		

	# return the node closest to given point
	def nearest(self, point, best=None):
	
		if self.pos is None:
			return best
	
		if best is None:
			best=self
			
		if self.dist(point) < best.dist(point):
			best=self
			
		if point[self.axis]<self.pos[self.axis]:
		
			best = self.left.nearest(point, best)
			# check if we have to follow recursion of the other side
			if self.dist_from_axis(point) < best.dist(point):
				best = self.right.nearest(point, best)
		
		else:
		
			best = self.right.nearest(point, best)
			if self.dist_from_axis(point) < best.dist(point):
				best = self.left.nearest(point, best)
			
			
		return best
			
		
	# returns how far this point is away from the axis this node is splitting
	def dist_from_axis(self, point):
		
		return abs(point[self.axis] - self.pos[self.axis])
		
			
	#TODO: remove
	def remove(self):
		pass
		
			
	
# tree factory	
def tree():

	return Node()
	
	
# returns a balanced version of that tree
def balanced(tree):

	nodes=[]
	for x in tree.inorder():
		nodes.append((x.pos, x.data))
		
	tree=Node()
	tree.addlist(nodes)
	return tree

	
def random():

	tree=Node()
	
	from random import randint as rnd
	
	for i in xrange(0,10):
		tree.add((rnd(0,10),rnd(0,10)),rnd(0,10))
		
	return tree
	
	
	
if __name__=='__main__':
	
	tree=tree()
	
	from random import randint as rnd
	
	for i in xrange(0,100000):
		tree.add((rnd(0,100000),rnd(0,100000)),rnd(0,100000))
		
	print "not balanced: ",tree.height(), tree.size()
	tree= balanced(tree)
	print "balanced: ",tree.height(), tree.size()
	
