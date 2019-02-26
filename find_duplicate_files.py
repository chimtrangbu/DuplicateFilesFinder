#!/usr/bin/env python3


import argparse
import hashlib
import json
import os


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('N', nargs='?', type=str,
                        help=argparse.SUPPRESS)
    options = parser.add_argument_group('Options')
    options.add_argument('-p', '--path', nargs=1, type=str,
                         help='accepts one mandatory argument that identifies '
                              'the root directory to start scanning for duplicate files')
    return parser.parse_args()


def scan_files(path):
    files = []
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.abspath(os.path.join(dirpath, f)))
    return files


def group_files_by_size(file_path_names):
    groups = {}
    for filename in file_path_names:
        size = os.path.getsize(filename)
        if size == 0:
            continue
        if size in groups.keys():
            groups[size].append(filename)
        else:
            groups[size] = [filename]
    return list(groups.values())


def get_file_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def group_files_by_checksum(file_path_names):
    groups = {}
    for filename in file_path_names:
        checksum = get_file_checksum(filename)
        if checksum in groups.keys():
            groups[checksum].append(filename)
        else:
            groups[checksum] = [filename]
    return list(groups.values())


def find_duplicate_files(file_path_names):
    groups_dup_files = []
    groups_by_size = group_files_by_size(file_path_names)
    for gr_by_size in groups_by_size:
        groups_by_checksum = group_files_by_checksum(gr_by_size)
        for gr_by_checksum in groups_by_checksum:
            if len(gr_by_checksum) > 1:
                groups_dup_files.append(gr_by_checksum)
    return json.dumps(groups_dup_files)

