import Resources

def createResource(restype, amount, mapnode):

	if restype==0:
	
		return Resources.Pillow(mapnode)
	
	elif restype==1:
		
		return Resources.Sterni(amount, mapnode)
		
	