import Resources

def createResource(restype, amount, mapnode):

	if restype==0:
	
		return Resources.Pillow(mapnode)
	
	elif restype==1:
		
		return Resources.Sterni(amount, mapnode)
		
	elif restype==2:
	
		return Resources.Busch(amount, mapnode)
		
	elif restype==3:
		
		return Resources.Hahn(mapnode)
		
	elif restype==4:
		
		return Resources.Blumenkohl(amount, mapnode)
		
	elif restype==5:
	
		return Resources.Pizza(amount, mapnode)
		
	elif restype==6:
	
		return Resources.Rock(mapnode)
