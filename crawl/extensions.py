import re

def normalize_element(extension):
	if re.search('^\.',extension):
		return extension
	else:
		return "." + extension