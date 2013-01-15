class NormalizedList(list):

	def append(self,value):
		value = self.normalize_element(value)
		super(NormalizedList,self).append(value)

	def extend(self,value):
		for val in value:
			val = self.normalize_element(val)

		super(NormalizedList,self).extend(value)

	def insert(self,index,value):
		value = self.normalize_element(value)
		super(NormalizedList,self).insert(index,value)

	def normalize_element(self,value):
		return value


