from distutils.core import setup
import os

long_description = "Python tool for finding files in a set of paths. Based on the Hike ruby gem"
if os.path.exists('README.txt'):
	long_description = open('README.txt').read()


setup(name='Crawl',
	  version='0.5.2',
	  url='https://github.com/OiNutter/crawl',
	  download_url='https://nodeload.github.com/OiNutter/crawl/legacy.tar.gz/master',
	  description='Python tool for finding files in a set of paths. Based on the Hike ruby gem',
	  long_description=long_description,
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