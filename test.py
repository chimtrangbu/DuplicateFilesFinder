from find_duplicate_files import *
import unittest
from os import chdir
from subprocess import getoutput as run
from requests import get
from filecmp import cmp


def get_file(url, filename=None):
    """
    download an online file
    :param url:
    :param filename: name to save in local
    :return:
    """
    response = get(url)
    if filename is None:
        filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(response.content)
    return


def duplicate_file(filename, nfiles):
    """
    copy file
    :param filename: name of original file
    :param nfiles: number of new copy-files
    :return:
    """
    for i in range(nfiles):
        if '.' in filename:
            name, file_type = filename.split('.', -1)
            run('cp %s %s' % (filename, name + str(i) + '.' + file_type))
        else:
            run('cp %s %s' % (filename, filename + str(i)))
    return


class TestFindDup(unittest.TestCase):
    def setUp(self):
        # test in folder test/
        run('mkdir test')
        chdir('test/')

        # test with empty files and dirs
        run('touch emptyfile .emptyhidden')
        run('ln -s emptyfile symlink2')
        run('mkdir emptydir')
        run('ln -s emptydir symlink0')
        run('mkdir dir_has_file')
        run('touch dir_has_file/file_init')
        run('ln -s dir_has_file symlink1')

        # test with different file-types and their duplicates
        run('echo the same size with file2 > samesize_file1')
        run('echo the same size with file1 > samesize_file2')

        get_file('https://intra.intek.io//uploads/material/file/'
                 'file/18/vietnam_cities.csv', 'testfile')
        duplicate_file('testfile', 2)
        get_file('https://intra.intek.io//uploads/material/file/'
                 'file/18/vietnam_cities.csv', 'testcsv.csv')

        get_file('https://arxiv.org/pdf/1609.04938v1.pdf', 'testpdf.pdf')
        duplicate_file('testpdf.pdf', 1)

        get_file('https://i.pinimg.com/originals/23/02/b7/'
                 '2302b739fe2bff298986a1801e156a0a.gif', 'testgif.gif')
        get_file('https://i.pinimg.com/originals/78/f5/a4/'
                 '78f5a40a3bc84a7ee16395f8be7dabc5.jpg', '.hidden')
        get_file('https://i.pinimg.com/originals/78/f5/a4/'
                 '78f5a40a3bc84a7ee16395f8be7dabc5.jpg', 'testjpg.jpg')

        get_file('https://cdn.freebiesupply.com/logos/large/2x/'
                 'eclipse-11-logo-png-transparent.png', 'testpng.png')
        duplicate_file('testpng.png', 2)

        run('mkdir a_same_size_gr')
        run('mv -t a_same_size_gr/ testfile testfile0 testfile1 testcsv.csv')

        # jump out
        chdir('../')

    def tearDown(self):
        run('rm -rf test/')

    def test_scan_files(self):
        out = str(scan_files('.'))
        self.assertIn("emptyfile'", out)
        self.assertNotIn("symlink2'", out)  # ignore symlinks
        self.assertIn(".emptyhidden'", out)
        self.assertIn(".hidden'", out)  # include hidden files
        self.assertNotIn("emptydir", out)  # ignore path of empty dir
        self.assertNotIn("symlink0", out)
        self.assertIn("dir_has_file/file_init'", out)
        self.assertNotIn("symlink1", out)  # ignore symlinks resolving to dirs

    def test_group_files_by_size(self):
        out = group_files_by_size(scan_files('.'))
        self.assertLess(1, min(map(len, out)))  # each gr has at least 2 files
        for group in out:  # all files in each group have the same size
            self.assertEqual(min(map(path.getsize, group)),
                             max(map(path.getsize, group)))
        self.assertIn(scan_files('./test/a_same_size_gr'), out)  # 1 case
        self.assertIn(['./test/samesize_file1', './test/samesize_file2'],
                      out)  # the same size but different content
        self.assertNotIn('empty', str(out))  # ignore empty files

    def test_group_files_by_checksum(self):
        out = group_files_by_checksum(scan_files('.'))
        self.assertLess(1, min(map(len, out)))  # each gr has at least 2 files
        for group in out:  # each group are duplicates
            for file in group:
                self.assertTrue(cmp(file, group[0]))
        self.assertNotIn('samesize', str(out))  # skip same-size but not dup

    def test_find_duplicate_files(self):
        out = find_duplicate_files(scan_files('.'))
        self.assertLess(1, min(map(len, out)))  # each gr has at least 2 files
        for group in out:  # each group are duplicates
            for file in group:
                self.assertTrue(cmp(file, group[0]))
        self.assertNotIn('empty', str(out))  # ignore empty files
        self.assertNotIn('samesize', str(out))  # skip same-size but not dup

    def test_group_files_by_comparing(self):
        out = group_files_by_comparing(scan_files('.'))
        self.assertLess(1, min(map(len, out)))  # each gr has at least 2 files
        for group in out:  # each group are duplicates
            for file in group:
                self.assertTrue(cmp(file, group[0]))
        self.assertNotIn('samesize', str(out))  # skip same-size but not dup

    def test_find_duplicate_files_bonus(self):
        out = find_duplicate_files(scan_files('.'))
        self.assertLess(1, min(map(len, out)))  # each gr has at least 2 files
        for group in out:  # each group are duplicates
            for file in group:
                self.assertTrue(cmp(file, group[0]))
        self.assertNotIn('empty', str(out))  # ignore empty files
        self.assertNotIn('samesize', str(out))  # skip same-size but not dup


if __name__ == '__main__':
    unittest.main()
