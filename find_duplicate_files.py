#!/usr/bin/env python3


from argparse import ArgumentParser
from hashlib import md5
from json import dumps
from os import path, walk


def parse_input():
    """
    parse input
    :return: arguments from console
    """
    parser = ArgumentParser()
    # Way_point 1:
    parser.add_argument('-p', '--path', type=str, required=True,
                        help='accepts one mandatory argument that '
                             'identifies the root directory to start '
                             'scanning for duplicate files')
    # Way_point 8:
    parser.add_argument('-b', '--bonus', type=bool,
                        help='another method to find duplicate files that '
                             'would be much faster than using hash algorithm')
    args = parser.parse_args()
    if not path.isdir(args.path):
        parser.print_help()
        exit(1)
    return args


def scan_files(path_dir):  # Way_point 2
    """
    :param path_dir: one argument path corresponding to an absolute path
    :return: a flat list of files scanned recursively from this specified path
    """
    files = []
    for dirpath, _, filenames in walk(path_dir):
        for f in filenames:
            path_file = path.join(dirpath, f)
            if not path.islink(path_file):  # ignore symbolic links
                files.append(path_file)
    return files


def group_files_by_size(file_path_names):  # Way_point 3
    """
    groups files by size
    :param file_path_names: mandatory argument, corresponding to a flat list
    of absolute file path names
    :return: a list of groups of at least two files that have the same size
    """
    groups = {}
    for filename in file_path_names:  # create the same-size-groups
        size = path.getsize(filename)
        if size == 0:
            continue  # ignore empty files
        if size in groups.keys():
            groups[size].append(filename)
        else:
            groups[size] = [filename]
    return [group for group in groups.values()
            if len(group) > 1]  # ignore if group has only 1 file


def get_file_checksum(file_path):  # Way_point 4
    """
    get md5 hash of file by MD5 message-digest algorithm
    :param file_path: path of a file
    :return: md5 hash
    """
    try:
        with open(file_path, "rb") as f:
            hash_md5 = md5(f.read())
        return hash_md5.hexdigest()
    except Exception:
        return None


def group_files_by_checksum(file_path_names):  # Way_point 5
    """
    group files by checksum
    :param file_path_names: one argument, corresponding to a flat list of
    the absolute path and name of files
    :return: a list of groups of duplicate files
    """
    groups = {}
    for filename in file_path_names:
        checksum = get_file_checksum(filename)
        if checksum is None:
            continue  # ignore broken link
        if checksum in groups.keys():
            groups[checksum].append(filename)
        else:
            groups[checksum] = [filename]
    return [group for group in groups.values()
            if len(group) > 1]  # ignore if group has only 1 file


def find_duplicate_files(file_path_names):  # Way_point 6
    """
    find duplicate files using group_files_by_size()
    and group_files_by_checksum()
    :param file_path_names: mandatory argument, corresponding to a list
    of absolute path and name of files
    :return: a list of groups of duplicate files
    """
    groups_dup_files = []
    for gr_by_size in group_files_by_size(file_path_names):
        groups_dup_files += group_files_by_checksum(gr_by_size)
    return [gr for gr in groups_dup_files if len(gr) > 1]


def compare_files(f1, f2):
    """
    compare contents of two files
    :param f1, f2: files to compare
    :return: True if they are duplicate files
    """
    try:
        bufsize = 4096  # 2^12
        with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
            while True:
                b1 = fp1.read(bufsize)
                b2 = fp2.read(bufsize)
                if b1 != b2:
                    return False
                if not b1:
                    return True
    except Exception:
        return False


def group_files_by_comparing(file_path_names):  # Way_point 8
    """
    group files by comparing contents of all files
    :param file_path_names: one argument, corresponding to a flat list of
    the absolute path and name of files
    :return: a list of groups of duplicate files
    """
    groups_dup_files = []
    file_paths = file_path_names.copy()
    while file_paths:
        cur_file = file_paths[0]
        gr_by_comparing = [cur_file]
        for filename in file_paths[1:]:
            if compare_files(cur_file, filename):
                gr_by_comparing.append(filename)
        file_paths = list(set(file_paths) - set(gr_by_comparing))
        if len(gr_by_comparing) > 1:
            groups_dup_files.append(gr_by_comparing)
    return groups_dup_files


def find_duplicate_files_bonus(file_path_names):
    """find duplicate files using group_files_by_size()
    and group_files_by_comparing()
    :param file_path_names: mandatory argument, corresponding to a list
    of absolute path and name of files
    :return: a list of groups of duplicate files
    """
    groups_dup_files = []
    for gr_by_size in group_files_by_size(file_path_names):
        groups_dup_files += group_files_by_comparing(gr_by_size)
    return [gr for gr in groups_dup_files if len(gr) > 1]


def main():
    args = parse_input()
    path_dir = args.path
    file_path_names = scan_files(path_dir)
    if args.bonus:
        groups_dup_files = find_duplicate_files_bonus(file_path_names)
    else:
        groups_dup_files = find_duplicate_files(file_path_names)
    print(dumps(groups_dup_files))  # Way_point 7


if __name__ == '__main__':
    main()
