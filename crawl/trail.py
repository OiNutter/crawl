from extensions import Extensions
import util
import os

class Trail:

	def __init__(self,root):
		self._root = str(root)
		self._extensions = [""]
		self._paths = [""]
		self._results = []

	def append_extension(self,extension):
		if extension not in self._extensions:
			self._extensions.append(Extensions.normalize_element(extension))

	def append_extensions(self,extensions):
		for ext in extensions:
			self.append_extension(Extensions.normalize_element(ext))

	def append_path(self,path):
		if path not in self._paths:
			self._paths.append(str(path))

	def append_paths(self,*args):
		for path in args:
			self.append_path(path)

	def find(self,target):
		self._results = []
		for path in self._paths:
			for ext in self._extensions:
				search_path = os.path.join(self._root,path,target + ext)
				search_path = os.path.abspath(search_path)
				if(os.path.exists(search_path)):
					self._results.append(str(search_path))
		
		return self._results

