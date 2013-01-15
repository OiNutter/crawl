from normalized_list import NormalizedList
import os

class Paths(NormalizedList):
	''' Paths is an internal collection for tracking path strings

		Relative paths added to this array are expanded relative to
		self.root

			paths = Paths(root="/user/local")
			paths.append("tmp")
			paths.append("/tmp")

			paths
			# => ["/usr/local/tmp","tmp"]
	'''

	def __init__(self,*args,**kwargs):
		self.root = kwargs.pop('root','.')
		super(Paths,self).__init__(*args,**kwargs)

	def normalize_element(self,path):
		if not os.path.isabs(path):
			path = os.path.join(self.root,path)

		return os.path.abspath(path)