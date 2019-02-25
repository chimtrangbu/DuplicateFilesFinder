#!/usr/bin/env python3


import argparse
import os
import glob


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('N', nargs='?', type=str,
                        help=argparse.SUPPRESS)
    options = parser.add_argument_group('Options')
    options.add_argument('-p', '--path', nargs=1, type=str,
                         help='accepts one mandatory argument that identifies the root directory to start scanning for duplicate files')
    return parser.parse_args()


def scan_files(path):
    files = []
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.abspath(os.path.join(dirpath, f)))
    return files


