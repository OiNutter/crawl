class NormalizedList(list):

	def __iadd__(self,value):
		value=self.normalize_element(value)
		super(NormalizedList,self).__iadd__(value)

	def __add__(self,value):
		value=self.normalize_element(value)
		return super(NormalizedList,self).__add__(value)

	def __setitem__(self,index,value):
		value=self.normalize_element(value)
		return super(NormalizedList,self).__setitem__(index,value)

	def __setslice__(self,start,finish,value):
		value[:] = [self.normalize_element(val) for val in value]
		return super(NormalizedList,self).__setslice__(start,finish,value)		

	def append(self,value):
		value = self.normalize_element(value)
		super(NormalizedList,self).append(value)

	def extend(self,value):
		value[:] = [self.normalize_element(val) for val in value]
		super(NormalizedList,self).extend(value)

	def insert(self,index,value):
		value = self.normalize_element(value)
		super(NormalizedList,self).insert(index,value)

	def normalize_element(self,value):
		return value


