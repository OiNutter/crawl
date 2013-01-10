from extensions import Extensions
import os

class Crawl:

	def __init__(self,root):
		self.root = str(root)
		self.extensions = [""]
		self.paths = [""]
		self.results = []

	def append_extension(self,extension):
		if extension not in self.extensions:
			self.extensions.append(Extensions.normalize_element(extension))

	def append_extensions(self,extensions):
		for ext in extensions:
			self.append_extension(Extensions.normalize_element(ext))

	def append_path(self,path):
		if path not in self.paths:
			self.paths.append(str(path))

	def append_paths(self,*args):
		for path in args:
			self.append_path(path)

	def find(self,target):
		self.results = []
		for path in self.paths:
			for ext in self.extensions:
				search_path = os.path.join(self.root,path,target + ext)
				search_path = os.path.abspath(search_path)
				if os.path.exists(search_path):
					self.results.append(str(search_path))
		
		return self.results

