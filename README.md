Crawl
=====

[![Build Status](https://travis-ci.org/OiNutter/crawl.png)](https://travis-ci.org/OiNutter/crawl)

Crawl is a port of the Ruby gem
[Hike](https://github.com/sstephenson/hike) to Python. Crawl will scan
through a list of given folders for a requested file. You can also specify
a list of possible extensions and aliases for those extensions.

Install
-------

```bash
$ pip install crawl
```

Usage
----

```python
import crawl
trail = crawl.Crawl()
trail.append_paths('lib','foo','bar')
trail.append_extensions('js','py')
trail.alias_extension('.coffee','.js')
trail.find('blah')
```

Getting Involved
----------------

If you want to get involved and help make Crawl better then please feel free. Just fork and clone the repo and install
any development requirements by running the following from the commmand line:

```bash
$ pip install -r dev_requirements.txt
```

Please write any necessary unit tests and check all tests still pass with your changes. If you want to discuss suggested changes
then please raise an issue, that way other people can discuss them as well. When you're happy everything is ready to go just submit
a pull request and I'll check it out.

###Running Tests###

Run the following from the command line to run all tests:

```bash
$ nosetests
```

Credits
-------

Huge amounts of credit to Sam Stephenson(@sstephenson) and Josh Peek(@josh) for all their work on the original 
[Hike](https://github.com/sstephenson/hike) gem. I have basically just rewritten their code and tests in python, tweaking where necessary to 
make things more 'pythonic' (I hope).

License
-------

Copyright 2012 Will McKenzie

Crawl is licensed under the MIT License, please see the LICENSE file for
more details.
