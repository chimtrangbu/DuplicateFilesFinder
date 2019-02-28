#!/usr/bin/env python3


import argparse
import hashlib
import json
from os import path, walk


def parse_input():
    parser = argparse.ArgumentParser()
    # Waypoint 1:
    parser.add_argument('-p', '--path', type=str, required=True,
                        help='accepts one mandatory argument that '
                             'identifies the root directory to start '
                             'scanning for duplicate files')
    args = parser.parse_args()
    if not path.isdir(args.path):
        parser.print_help()
        exit(1)
    return args


def scan_files(path_dir):  # Waypoint 2
    files = []
    for dirpath, _, filenames in walk(path_dir):
        for f in filenames:
            path_file = path.abspath(path.join(dirpath, f))
            if not path.islink(path_file):  # ignore symbolic links
                files.append(path_file)
    return files


def group_files_by_size(file_path_names):  # Waypoint 3
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


def get_file_checksum(file_path):  # Waypoint 4
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except FileNotFoundError:
        return None
    return hash_md5.hexdigest()


def group_files_by_checksum(file_path_names):  # Waypoint 5
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


def find_duplicate_files(file_path_names):  # Waypoint 6
    groups_dup_files = []
    groups_by_size = group_files_by_size(file_path_names)
    for gr_by_size in groups_by_size:
        groups_by_checksum = group_files_by_checksum(gr_by_size)
        for gr_by_checksum in groups_by_checksum:
            if len(gr_by_checksum) > 1:
                groups_dup_files.append(gr_by_checksum)
    return json.dumps(groups_dup_files)  # Waypoint 7


def compare_files(f1, f2):
    bufsize = 2048
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True


def group_by_comparing(file_path_names):
    return [(i, j) for i in file_path_names for j in file_path_names if (compare_files(i, j)).all() and i != j]



def main():
    args = parse_input()
    path = args.path
    file_path_names = scan_files(path)
    groups_dup_files = find_duplicate_files(file_path_names)
    print(groups_dup_files)


if __name__ == '__main__':
    main()
