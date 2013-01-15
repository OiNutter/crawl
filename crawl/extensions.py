import re
from normalized_list import NormalizedList


class Extensions(NormalizedList):
	''' Extensions is an internal collection for tracking extension names. 

		Extensions added to this array are normalized with a leading `.`

			extensions.append("js")
			extensions.append(".css")

			extensions
			# => [".js",".css"]

	'''
	
	def normalize_element(self,extension):

		if re.search('^\.',extension):
			return extension
		else:
			return "." + extension