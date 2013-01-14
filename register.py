import pandoc

pandoc.core.PANDOC_PATH = "pandoc"

doc = pandoc.Document()
doc.markdown = open('README.md','r').read()
f = open('README.txt','w+')
f.write()
f.close()
os.system("setup.py register")
os.remove('README.txt')