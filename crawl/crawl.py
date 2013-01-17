import os

from index import Index
from paths import Paths
from extensions import Extensions

class Crawl:

	def __init__(self,root="."):
		self.root = os.path.abspath(root)
		self.paths = Paths(root=self.root)
		self.extensions = Extensions()
		self.aliases = {}

	def prepend_paths(self,*paths):
		new = Paths(paths)
		new.extend(self.paths)
		self.paths = new

	def prepend_path(self,*paths):
		self.prepend_paths(*paths)

	def append_paths(self,*paths):
		for path in paths:
			self.paths.append(path)

	def append_path(self,*paths):
		self.append_paths(*paths)

	def remove_path(self,path):
		if path in self.paths:
			self.paths.remove(path)

	def prepend_extensions(self,*extensions):
		new = Extensions(extensions)
		new.extend(self.extensions)
		self.extensions = new

	def prepend_extension(self,*extensions):
		self.prepend_extensions(*extensions)

	def append_extensions(self,*extensions):
		for extension in extensions:
			self.extensions.append(extension)

	def append_extension(self,*extensions):
		self.append_extensions(*extensions)

	def remove_extension(self,extension):
		if extension in self.extensions:
			self.extensions.remove(extension)

	def alias_extension(self,new_extension,old_extension):
		new_extension = self.extensions.normalize_element(new_extension)

		self.aliases[new_extension] = self.extensions.normalize_element(old_extension)

	def unalias_extension(self,extension):
		del self.aliases[self.extensions.normalize_element(extension)]

	def find(self,*args,**kwargs):
		return self.index().find(*args,**kwargs)

	def index(self):
		return Index(self.root,self.paths,self.extensions,self.aliases)

	def entries(self,*args):
		return self.index().entries(*args)

	def stat(self,*args):
		return self.index().stat(*args)