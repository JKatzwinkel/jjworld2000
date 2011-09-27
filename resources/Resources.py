import Resource


class Pillow(Resource.Resource):

	def __init__(self, mapnode):
	
		Resource.Resource.__init__(self, 0, 1, mapnode)
		self.initImages()
		self.maxAmount=1
		

class Sterni(Resource.Resource):

	def __init__(self, amount, mapnode):
		
		Resource.Resource.__init__(self, 1, amount, mapnode)
		self.initImages()
		self.maxAmount=20
		
		
		
		
