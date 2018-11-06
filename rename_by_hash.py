#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import hashlib
import sys

path = '' # add path

def get_file_path(dir_path):
    all_file = os.listdir(dir_path)
    all_file_path = []
    for i in range(len(all_file)):
        all_file_path.append(dir_path + all_file[i])
    return all_file_path

def get_hash(file_path):
    algo = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            algo.update(data)
    return algo.hexdigest()

def rename(path):
    all_path = get_file_path(path)[:]
    for i in range(len(all_path)):
        each_file_path = all_path[i]
        if 'tar.xz' not in each_file_path:
            if '.tgz' not in each_file_path:
                continue
        a = get_hash(each_file_path)
        os.rename(each_file_path, path + a)
        print('rename ' + each_file_path + ' to ' + a)

if __name__ == '__main__':
    rename(path)