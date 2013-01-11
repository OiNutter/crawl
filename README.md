Crawl
=====

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

License
-------

Copyright 2012 Will McKenzie

Crawl is licensed under the MIT License, please see the LICENSE file for
more details.
