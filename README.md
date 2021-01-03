# GitMC -- concurrent asynchronous Git Utilities for operations on massive numbers of Git repos

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3339891.svg)](https://doi.org/10.5281/zenodo.3339891)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/gitMC.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/gitMC/context:python)
![Actions Status](https://github.com/scivision/gitmc/workflows/ci/badge.svg)
![CodeQL](https://github.com/scivision/gitmc/workflows/CodeQL/badge.svg)
[![pypi versions](https://img.shields.io/pypi/pyversions/gitutils.svg)](https://pypi.python.org/pypi/gitutils)
[![PyPi Download stats](http://pepy.tech/badge/gitutils)](http://pepy.tech/project/gitutils)

Platform-independent (Linux/Mac/Windows) Git utilities, useful for managing large (100+) numbers of Git repos.
Speed is an emphasis throughout, with concurrency via Python `asyncio` and pipelining.
In general, GitMC works with all GitHub repos, including organization private repos--assuming you have created a GitHub Oauth key with appropriate permissions ("repo" needed for private org/user repos").

GitMC uses command-line Git because PyGit also requires command-line Git installed, and we don't need the advanced functionality.

---

Also see
[PyGit-bulk](https://github.com/scivision/pygit-bulk)
for managing large (100+) numbers of users / teams.

## Install

Install Git in a way accessible from the command line line

* Mac: `brew install git`
* Linux: `apt install git`
* Windows: command line [Git](https://git-scm.com/download/win).

```sh
python -m pip install -e .
```

## Usage

* `gitbranch` Tells of any non-master branches under directory ~/code
* `gitemail` list all contributor email addresses. To fix unwanted emails use [Git-filter-repo](https://www.scivision.dev/git-update-email-address/)
* `find_missing_file`: find directories missing exact fullpath to file
* `find_matching_file`: find directories matching exact fullpath to file

### Sync large number of git repos

These assume numerous subdirectories under `~/code`.
They work very quickly for large numbers (100+) of repos.

* `gitstat` check if any local repos have pending changes
* `gitpull` Git pulls all repos (suggest `gitfetch` instead)
* `gitfetch` Git fetches all repos, printing a summary of files changed on remote

Place an empty file `.nogit` in a subdirectory to skip it.

#### [optional] speedup with https pull

For public repos, to make the Git remote checking go at least twice as fast, and significantly reduce the computational burden when SSH is used for `git push` (as is recommended), consider the "pushInsteadOf" global Git config.
To do this, when cloning a public repo (including ones you're a collaborator on), use `git clone https://`.
This global SSH push config one-time does SSH push for HTTPS-cloned repos:

```sh
git config --global url."ssh://github.com/".pushInsteadOf https://github.com/
```

The pattern matching can be made for all sites by omitting `github.com` from the command above, or you can refine it for each site, or even for specific usernames by editing the command above.
For private repos, simply clone with SSH as usual

### Preview all changed Jekyll files

This is for a website made using
[Jekyll](https://www.scivision.dev/create-jekyll-github-pages-website)
or
[Hugo](https://github.com/scivision/hugo-flex-example):

```sh
ActOnChanged . -p
```

It shows web page previews of all pages changed locally--start the Jekyll or Hugo debug server first e.g. `hugo serve`
