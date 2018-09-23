from time import sleep
from pathlib import Path
import pandas
import subprocess
import tempfile
import logging
import github
from .github_base import github_session, check_api_limit, repo_exists


def repo_dupe(fn: Path, oauth: Path, orgname: str = '', stem: str = ''):
    """
    fn: .xlsx file with repos to duplicate
    oauth: Path to your GitHub Oauth token  https://github.com/settings/tokens
    orgname: create repos under Organization instead of username
    stem: what to start new repo name with
    """
# %% authenticate
    sess = github_session(oauth)
    guser = sess.get_user()

    org = None
    if orgname:
        orgs = list(guser.get_orgs())
        for o in orgs:
            if o.login == orgname:
                org = o
                break

        assert org is not None
        op = org
    else:
        op = guser

    username = op.login

    if not check_api_limit(sess):
        raise RuntimeError('GitHub API limit exceeded')
# %% get list of repos to duplicate
    fn = Path(fn).expanduser()
    repos = pandas.read_excel(fn, index_col=0, usecols="A, D")
    repos.dropna(how='any', inplace=True)
# %% prepare to loop over repos
    for email, row in repos.iterrows():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        oldurl = row.item()
        olduser, oldname = oldurl.split('/')[-2:]
        oldname = oldname.split('.')[0]
        try:
            oldrepo = sess.get_user(olduser).get_repo(oldname)
        except github.GithubException as e:
            logging.error(f'{oldurl} not found \n')

        try:
            oldrepo.get_contents('/')
        except github.GithubException as e:
            logging.error(f'{oldurl} is empty. \n')

        mirrorname = stem + email
        newname = f'{username}/{mirrorname}'
        newurl = f'ssh://github.com/{newname}'

        exists = repo_exists(op, mirrorname)
        if exists:
            newrepo = op.get_repo(mirrorname)
            if newrepo.pushed_at >= oldrepo.pushed_at:
                continue

        print('\n', email, oldurl, '\n')
        with tempfile.TemporaryDirectory() as d:
            tmprepo = Path(d)
            # 1. bare clone
            subprocess.check_call(['git', 'clone', '--bare', oldurl],
                                  stdout=subprocess.DEVNULL, cwd=tmprepo)

            # 2. create new repo
            if not exists:
                op.create_repo(name=mirrorname, private=True)

            # 3. mirror to new repo
            pwd = (tmprepo / (oldurl.split('/')[-1])).with_suffix('.git')
            cmd = ['git', 'push', '--mirror', newurl]
            subprocess.check_call(cmd, cwd=pwd)

        sleep(0.1)