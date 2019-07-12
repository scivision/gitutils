#!/usr/bin/env python
import subprocess
from pathlib import Path
from gitutils.push import coro_local
from gitutils.runner import runner

R = Path(__file__).parent


def test_script():
    subprocess.check_call(['gitmodified', str(R.parent)])


def test_mod():

    repos = runner(coro_local, R.parent)
    assert len(repos) in {0, 1}
