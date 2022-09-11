#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def count_cjk():
    """Count the number of CJK characters in the dump"""
    count = 0
    dump_dir = "dump/"
    for filename in os.listdir(dump_dir):
        with open(dump_dir + filename, "r") as f:
            for line in f:
                for cp in line:
                    if is_cjk_cp(ord(cp)):
                        count += 1
    return count


def is_cjk_cp(cp):
    return (
        (0x3400 <= cp <= 0x4DBF)
        or (0x4E00 <= cp <= 0x9FFF)
        or (0xF900 <= cp <= 0xFAFF)
        or (0x20000 <= cp <= 0x2FFFF)
    )


if __name__ == "__main__":
    print(count_cjk())
