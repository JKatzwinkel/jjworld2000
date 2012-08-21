import Resources

def createResource(restype, mapnode, amount):

	if restype==0:
	
		return Resources.Pillow(mapnode)
	
	elif restype==1:
		
		return Resources.Sterni(mapnode, amount)
		
	elif restype==2:
	
		return Resources.Busch(mapnode, amount)
		
	elif restype==3:
		
		return Resources.Hahn(mapnode)
		
	elif restype==4:
		
		return Resources.Blumenkohl(mapnode, amount)
		
	elif restype==5:
	
		return Resources.Pizza(mapnode, amount)
		
	elif restype==6:
	
		return Resources.Rock(mapnode)
		
	elif restype==7:
	
		return Resources.Pumpkin(mapnode, amount)
