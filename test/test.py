import sys
sys.path.insert(0,'../')

import crawl
trail = crawl.Crawl('/')
trail.append_paths('../')
trail.append_extensions('.py')
print trail.find('crawl/registry')