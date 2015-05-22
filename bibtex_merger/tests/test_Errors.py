import unittest, sys, os

python2 = sys.version_info < (3, 0, 0)

if python2:
    from StringIO import StringIO
else:
    from io import StringIO

from bibtex_merger.errors import *

class TestErrors(unittest.TestCase):
	def test_base(self):
		self.assertEqual(2 + 2, 4)