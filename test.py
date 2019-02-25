from find_duplicate_files import *

# paths = scan_files('~/Pictures')
# print(len(paths))
# for p in paths:
#     print(p)


import unittest
from subprocess import getoutput as run


class TestFindDup(unittest.TestCase):
    def setUp(self):
        run('touch abc xyz')

    def tearDown(self):
        run('rm abc xyz')

    def test_scan_files(self):
        out = str(scan_files('.'))
        self.assertIn('abc', out)
        self.assertIn('xyz', out)


if __name__ == '__main__':
    unittest.main()
