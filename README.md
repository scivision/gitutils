[![image](https://travis-ci.org/scivision/pygitutils.svg?branch=master)](https://travis-ci.org/scivision/pygitutils)
[![image](https://coveralls.io/repos/github/scivision/pygitutils/badge.svg?branch=master)](https://coveralls.io/github/scivision/pygitutils?branch=master)
[![image](https://ci.appveyor.com/api/projects/status/peeed6kh6p59w4kb?svg=true)](https://ci.appveyor.com/project/scivision/pygitutils)
[![Maintainability](https://api.codeclimate.com/v1/badges/f75c5317665dc32298a4/maintainability)](https://codeclimate.com/github/scivision/pygitutils/maintainability)
[![pypi versions](https://img.shields.io/pypi/pyversions/pygitutils.svg)](https://pypi.python.org/pypi/pygitutils)
[![pypi format](https://img.shields.io/pypi/format/pygitutils.svg)](https://pypi.python.org/pypi/pygitutils)
[![PyPi Download stats](http://pepy.tech/badge/pygitutils)](http://pepy.tech/project/pygitutils)

# Python Git utils

Platform-independent (Linux/Mac/Windows) Git utilities, useful for managing large (100+) numbers of Git repos. 
I use command-line git because PyGit also requires command-line Git installed, and I don't need the advanced functionality.

For embedded systems using system Python such as the Raspberry Pi, you
can set the default Python to Python 3 using
[update-alternatives](https://www.scivison.co/set-python-version-update-alternatives).

## Prereq

Install Git in a way accessible from the command line line

-   Mac: `brew install git`
-   Linux: `apt install git`
-   Windows: command line [Git](https://git-scm.com/download/win).
-   BSD: `pkg install git`

## Install

    python -m pip install -e . 



## Sync large number of git repos in subdirectories

These assume numerous subdirectories under `~/code` or `c:\code`. They
work very quickly for large numbers (100+) repos

program  | description
---------|-----------------------------------------
gtps.py  | check if any repos have pending changes
gtpl.py  | `git pull` all repos
gtft.py  | `git fetch` all repos

You can place an empty file `.nogit` in a subdirectory if you don't want
it to be checked for `pull` or `push`. For `gtps.py`, the changed files
are noted--you have to `cd` to that directory and commit/push as usual.

## Program listing

  Program                | Function
-------------------------|------------------------------------------------------------------
  gtpl.py                |  Pulls all git repos under directory ~/code
  gtps.py                |  Pushes " " " " " "
  gtft.py                |  Fetches " "
  gitbranch              | Tells of any non-master branches under directory ~/code
  git_filemode_windows   | Sets all git repos to don't care permissions under directory ~/code
  gitemail.py            |  list all contributor email addresses. Optionally, amend email addresses for prior Git commits
  ActOnChanged.py        |  print list of changed files OR run a program to edit/view them

### Preview all changed Jekyll files

This is for a website made using
[Jekyll](https://www.scivision.co/create-jekyll-github-pages-website):
```sh
ActOnChanged.py --jekyll
```
