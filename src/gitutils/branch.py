"""
Operations for Git branches

git branch get name methods:
https://stackoverflow.com/a/45028375
"""

import argparse
import typing as T
from pathlib import Path
import asyncio
import logging
import subprocess

from . import _log
from .git import GITEXE, gitdirs

BRANCH_REV = ["rev-parse", "--abbrev-ref", "HEAD"]
BRANCH_SYM = ["symbolic-ref", "--short", "HEAD"]
BRANCH_NAME = ["name-rev", "--name-only", "HEAD"]
BRANCH_SIMPLE = ["branch", "--show-current"]  # Git >= 2.22
SWITCH = ["switch"]


async def different_branch(main: T.Sequence[str], path: Path) -> T.Tuple[str, str]:
    """
    does branch not match specified name

    Parameters
    ----------

    main : str
        desired default branch name
    path : pathlib.Path
        Git repo to check

    Returns
    -------

    branch : tuple of pathlib.Path, str
        repo path and branch name
    """

    proc = await asyncio.create_subprocess_exec(
        *[GITEXE, "-C", str(path)] + BRANCH_SIMPLE, stdout=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {BRANCH_SIMPLE}")
    logging.info(str(path))

    branch_name = stdout.decode("utf8").strip()

    if isinstance(main, str):
        main = [main]

    if branch_name not in main:
        return path.name, branch_name

    return None


async def git_branch(branch: T.Sequence[str], path: Path) -> T.List[T.Tuple[str, str]]:

    different = []
    for r in asyncio.as_completed([different_branch(branch, d) for d in gitdirs(path)]):
        diff = await r
        if diff:
            different.append(diff)
            print(diff)

    return different


def branch_switch(path: Path, old_branch: str, new_branch: str):

    for d in gitdirs(path):
        cmd = [GITEXE, "-C", str(d)] + BRANCH_SIMPLE
        current = subprocess.check_output(cmd, text=True, timeout=5).strip()
        if current == new_branch:
            continue
        if current != old_branch:
            logging.info(f"not changing: {d.name}: {current} != {old_branch}")
            continue

        cmd = [GITEXE, "-C", str(d)] + BRANCH_SIMPLE
        ret = subprocess.run(
            [GITEXE, "-C", str(d)] + SWITCH + [new_branch],
            stderr=subprocess.PIPE,
            timeout=10,
            text=True,
        )
        if ret.returncode != 0:
            stderr = ret.stderr.strip()
            if stderr == f"fatal: invalid reference: {new_branch}":
                continue
            else:
                raise ValueError(
                    f"{d} could not switch to {new_branch} from {old_branch}: {stderr}"
                )

        print(d.name, old_branch, "=>", new_branch)


def cli():
    """
    report on git repos not on the expected branch e.g. 'master'
    """

    p = argparse.ArgumentParser(
        description="check for non-default branches, and mass switch branches"
    )
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-main", nargs="+", default=["main", "master"], help="name of your main branch")
    p.add_argument("-switch", nargs=2, help="switch branch from OLD to NEW, if NEW is available")
    P = p.parse_args()

    _log(P.verbose)

    if P.switch is None:
        asyncio.run(git_branch(P.main, P.path))
    else:
        branch_switch(P.path, *P.switch)


if __name__ == "__main__":
    cli()
