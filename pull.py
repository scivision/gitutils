#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git pull" each of them.
"""
from gitutils import fetchpull
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    P = p.parse_args()

    for new_remote in fetchpull('pull', P.codepath):
        # no backslash allowed in f-strings
        print(new_remote)


if __name__ == '__main__':
    main()
