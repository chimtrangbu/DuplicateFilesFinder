from find_duplicate_files import *
import unittest
import os
from subprocess import getoutput as run
import requests


def get_file(url, filename=None):
    response = requests.get(url)
    if filename is None:
        filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(response.content)
    return


def duplicate_file(filename, nfiles):
    for i in range(nfiles):
        if '.' in filename:
            name, type = filename.split('.', -1)
            run('cp %s %s' % (filename, name + str(i) + '.' + type))
        else:
            run('cp %s %s' % (filename, filename + str(i)))
    return


class TestFindDup(unittest.TestCase):
    def setUp(self):
        # test in folder test/
        run('mkdir test')
        os.chdir('test/')

        # test with empty files and dirs
        run('touch emptyfile .emptyhidden')
        run('ln -s emptyfile symlink2')
        run('mkdir emptydir')
        run('ln -s emptydir symlink0')
        run('mkdir dir_has_file')
        run('touch dir_has_file/file_init')
        run('ln -s dir_has_file symlink1')

        # test with different file-types and their duplicates
        get_file('https://intra.intek.io//uploads/material/file/file/18/vietnam_cities.csv', 'testfile')
        duplicate_file('testfile', 2)
        get_file('https://intra.intek.io//uploads/material/file/file/18/vietnam_cities.csv', 'testcsv.csv')
        get_file('https://arxiv.org/pdf/1609.04938v1.pdf', 'testpdf.pdf')
        duplicate_file('testpdf.pdf', 1)
        get_file('https://i.pinimg.com/originals/23/02/b7/2302b739fe2bff298986a1801e156a0a.gif', 'testgif.gif')
        get_file('https://i.pinimg.com/originals/78/f5/a4/78f5a40a3bc84a7ee16395f8be7dabc5.jpg', '.hidden')
        get_file('https://i.pinimg.com/originals/78/f5/a4/78f5a40a3bc84a7ee16395f8be7dabc5.jpg', 'testjpg.jpg')
        get_file('https://cdn.freebiesupply.com/logos/large/2x/eclipse-11-logo-png-transparent.png', 'testpng.png')
        duplicate_file('testpng.png', 2)

        # jump out
        os.chdir('../')

    def tearDown(self):
        run('rm -rf test/')

    def test_scan_files(self):
        out = str(scan_files('.'))
        self.assertIn("emptyfile'", out)
        self.assertIn("symlink2'", out)
        self.assertIn(".emptyhidden'", out)
        self.assertIn(".hidden'", out)
        self.assertNotIn("emptydir", out)
        self.assertNotIn("symlink0", out)
        self.assertIn("dir_has_file/file_init'", out)
        self.assertNotIn("symlink1/file_init'", out)

    def test_group_files_by_size(self):
        out = group_files_by_size(scan_files('test'))
        self.assertNotIn('?', out)


if __name__ == '__main__':
    unittest.main()
