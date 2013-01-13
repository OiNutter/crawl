from distutils.core import setup
import pandoc

pandoc.core.PANDOC_PATH = "pandoc"

doc = pandoc.Document()
doc.markdown = open('README.md','r').read()
setup(name='Crawl',
	  version='0.4',
	  url='https://github.com/OiNutter/crawl',
	  download_url='https://nodeload.github.com/OiNutter/crawl/legacy.tar.gz/master',
	  description='Python tool for finding files in a set of paths. Based on the Hike ruby gem',
	  long_description=doc.rst,
	  author='Will McKenzie',
	  author_email='will@oinutter.co.uk',
	  packages=['crawl'],
	  package_dir={'crawl': 'crawl'},
	  license='MIT License',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
        ]
	)