import os
import re
import copy

class Index:

	def __init__(self,root,paths,extensions,aliases):
		self.root = root
		self.extensions = copy.deepcopy(extensions)
		self.aliases= copy.deepcopy(aliases)
		self.paths = copy.deepcopy(paths)
		self.entries_cache = {}
		self.stat_cache = {}
		self.patterns = {}

	def index(self):
		return self

	def is_relative_path(self,path):
		return True if re.match(r"""^\.\.?\/""",path) else False

	def entries(self,path):
		
		if not self.entries_cache.has_key(path):

			entries = []

			if os.path.exists(path) and os.path.isdir(path):
					entries = os.listdir(path)

			self.entries_cache[path] = [filename for filename in entries if not re.search(r"""^\.|~$|^\#.*\#$""",filename)]

		return copy.deepcopy(self.entries_cache[path])

	def stat(self,path):

		if not self.stat_cache.has_key(path):
			self.stat_cache[path] = os.stat(path) if os.path.exists(path) else None

		return copy.deepcopy(self.stat_cache[path])

	def find(self,*logical_paths,**kwargs):

		if kwargs.has_key('callback') and kwargs['callback']:
			base_path = kwargs.get('base_path',self.root)

			results = []
			for path in logical_paths:
				path = re.sub(r"""^/""",'',path)

				if not self.is_relative_path(path):
					result = self.find_in_paths(path)
				else:
					result = self.find_in_base_path(path,base_path)

				if result:
					results.extend(result)

			return kwargs['callback'](results)

		else:
			kwargs['callback'] = lambda paths:paths[0] if paths else None
			return self.find(*logical_paths,**kwargs)

	def find_in_paths(self,path):

		dirname,basename = os.path.split(path)

		results = []
		for search_path in self.paths:
			result = self.match(os.path.join(search_path,dirname),basename)
			if result:
				results.extend(result)

		return results

	def find_in_base_path(self,path,base_path):

		candidate = os.path.join(base_path,path)
		dirname,basename = os.path.split(candidate)
		return self.match(dirname,basename) if self.do_paths_contain(dirname) else None

	def do_paths_contain(self,dirname):
		matches = [path for path in self.paths if str(dirname)[0:len(path)] == path]
		return True if matches else False

	def match(self,dirname,basename):
		
		matches = self.entries(dirname)
		pattern = self.get_pattern_for(basename)

		matches[:] = [match for match in matches if pattern.match(match)]

		results = []
		for path in self.sort_matches(matches,basename):
			pathname = os.path.abspath(os.path.join(dirname,path))

			if os.path.isfile(pathname):
				results.append(pathname)

		return results

	def get_pattern_for(self,basename):
		if self.patterns.has_key(basename):
			return self.patterns[basename]
		else:
			pattern = self.build_pattern_for(basename)
			self.patterns[basename] = pattern
			return pattern

	def build_pattern_for(self,basename):

		filename, ext = os.path.splitext(basename.lower())
		aliases = self.find_aliases_for_ext(self.extensions.normalize_element(ext))

		basename_re = re.escape(basename)

		if aliases:
			aliases.insert(0,ext)
			basename_re = "%s(%s)" % (re.escape(filename),'|'.join([re.escape(ext) for ext in aliases]))

		extension_pattern = '|'.join([re.escape(ext) for ext in self.extensions])
		return re.compile(r"""^%s(?:%s)*$""" % (basename_re,extension_pattern))

	def find_aliases_for_ext(self,ext):

		exts = []

		for alias,original in self.aliases.iteritems():

			if original == ext:
				exts.append(alias)

		return exts

	def sort_matches(self,matches,basename):
		filename,ext = os.path.splitext(basename)
		aliases = self.find_aliases_for_ext(ext)

		def sort_func(match):
			name = re.sub(basename,'',match)
			extnames = re.findall(r"""\.[^.]+""",name)
			score = 0
			for ext in extnames:
				ext
				if ext in self.extensions:
					score += self.extensions.index(ext) + 1
				elif ext in aliases:
					score += aliases.index(ext) + 11
			
			return score

		return sorted(matches,key=sort_func)