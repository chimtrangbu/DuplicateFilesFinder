from find_duplicate_files import *
import unittest
import os
from subprocess import getoutput as run


class TestFindDup(unittest.TestCase):
    def setUp(self):
        # test scan_files
        run('mkdir test')
        os.chdir('test/')
        run('touch file1 .hidden')
        run('ln -s file1 symlink1')
        run('mkdir emptydir')
        run('ln -s emptydir symlink0')
        os.chdir('../')

        # test group_files_by_size
        run('python3 generate_duplicate_files.py -p test')

    def tearDown(self):
        run('rm -rf test')

    def test_scan_files(self):
        out = str(scan_files('/home/hminhanh/DuplicateFilesFinder/test'))
        self.assertIn("file1'", out)
        self.assertIn("symlink1'", out)
        self.assertIn(".hidden'", out)
        self.assertNotIn("emptydir", out)
        self.assertNotIn("symlink0", out)

    def test_group_files_by_size(self):
        out = group_files_by_size(scan_files('test'))
        self.assertIn('?', '?')


if __name__ == '__main__':
    unittest.main()
