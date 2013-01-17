Crawl
=====

[![Build Status](https://travis-ci.org/OiNutter/crawl.png)](https://travis-ci.org/OiNutter/crawl)

Crawl is a port of the Ruby gem
[Hike](https://github.com/sstephenson/hike) to Python. Crawl will scan
through a list of given folders for a requested file. You can also
configure it to just match any of a given list of extensions.

While Crawl does work at the basic level, it is not yet a complete port
of Hike, as it doesn't implement Hike's index caching for speedier
responses, although I do intend to add that.

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

License
-------

Copyright 2012 Will McKenzie

Crawl is licensed under the MIT License, please see the LICENSE file for
more details.
