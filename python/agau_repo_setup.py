# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2023 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Agile Authoring repos set-up."""

import argparse
import logging
import os
import pathlib
import subprocess  # noqa: S404
import tempfile
from typing import Dict

import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname).1s %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

GH_TOKEN = 'GH_TOKEN'  # noqa: S105
REPLACE_ME = 'REPLACE_ME'


def validate_gh() -> None:
    """Validate gh, git commands and GH_TOKEN exist."""
    output = subprocess.getoutput('gh --help')
    if 'USAGE' not in output:
        raise RuntimeError('gh command not available?')
    output = subprocess.getoutput('git --help')
    if 'usage' not in output:
        raise RuntimeError('git command not available?')
    gh_token = os.getenv(GH_TOKEN)
    if not gh_token:
        raise RuntimeError(f'environment variable {GH_TOKEN} not found? (hint: export GH_TOKEN=<your-GITHUB-token>)')


def validate_oscal_type(repo_name: str, repo_oscal_type: str) -> None:
    """Validate oscal type."""
    if not repo_oscal_type:
        raise RuntimeError(f'{repo_name} "oscal-type" missing')


def get_yaml(config: str) -> Dict:
    """Get yaml data from config file."""
    with open(config, 'r') as stream:
        try:
            ydata = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise RuntimeError(exc)
    validate_yaml(ydata)
    return ydata


def validate_yaml(ydata: Dict) -> None:
    """Validate yaml."""
    git = ydata.get('git')
    if not git:
        raise RuntimeError('yaml missing "git"')
    scheme = git.get('scheme')
    if not scheme:
        raise RuntimeError('yaml missing "git scheme"')
    domain = git.get('domain')
    if not domain:
        raise RuntimeError('yaml missing "git domain"')
    owner = git.get('owner')
    if not owner:
        raise RuntimeError('yaml missing "git owner"')
    if owner == REPLACE_ME:
        raise RuntimeError(f'yaml invalid "git owner" = {owner}')
    email = ydata.get('email')
    if not email:
        raise RuntimeError('yaml missing "email"')
    name = email.get('name')
    if not name:
        raise RuntimeError('yaml missing "email name"')
    address = email.get('address')
    if not address:
        raise RuntimeError('yaml missing "email address"')
    repos = ydata.get('repos')
    if not repos:
        raise RuntimeError('yaml missing "repos"')


def normalize(url_part: str) -> str:
    """Normalize."""
    rval = url_part + ''
    if rval.endswith('/'):
        rval = rval.rsplit('/', 1)[0]
    return rval


def synthesize_repo_url(git_scheme: str, git_domain: str, git_owner: str, repo_name: str) -> str:
    """Synthesize repo URL."""
    url = f'{normalize(git_scheme)}://{normalize(git_domain)}/{normalize(git_owner)}/{normalize(repo_name)}'
    return url


def update_config_env(
    config_env_path: pathlib.Path,
    repo_oscal_type: str,
    git_owner: str,
    repo_name: str,
    downstream: str,
    email_name: str,
    email_address: str
) -> None:
    """Update config.env."""
    with open(config_env_path, 'r') as f:
        lines = f.readlines()
    with open(config_env_path, 'w') as f:
        for line in lines:
            if repo_oscal_type == 'catalog':
                line = line.replace('CATALOG=catalog-folder', f'CATALOG={repo_name}')
                line = line.replace('REPO_BASE=my-repo-base', f'REPO_BASE={git_owner}')
                line = line.replace('REPO_PROFILE=my-profile', f'REPO_PROFILE={downstream}')
                line = line.replace('NAME=Automation-Bot', f'NAME={email_name}')
                line = line.replace('EMAIL=automation@example.com', f'EMAIL={email_address}')
                f.write(line)
            elif repo_oscal_type == 'profile':
                line = line.replace('PROFILE=profile-folder', f'PROFILE={repo_name}')
                line = line.replace('REPO_BASE=my-repo-base', f'REPO_BASE={git_owner}')
                line = line.replace('REPO_COMPONENT_DEFINITION=my-component-definition', f'REPO_PROFILE={downstream}')
                line = line.replace('NAME=Automation-Bot', f'NAME={email_name}')
                line = line.replace('EMAIL=automation@example.com', f'EMAIL={email_address}')
                f.write(line)
            elif repo_oscal_type == 'component-definition':
                line = line.replace(
                    'COMPONENT_DEFINITION=component-definition-folder', f'COMPONENT_DEFINITION={repo_name}'
                )
                line = line.replace('REPO_BASE=my-repo-base', f'REPO_BASE={git_owner}')
                line = line.replace(
                    'REPO_COMPONENT_DEFINITION=my-component-definition', f'REPO_COMPONENT_DEFINITION={repo_name}'
                )
                line = line.replace(
                    'REPO_SYSTEM_SECURITY_PLAN=my-system-security-plan', f'REPO_SYSTEM_SECURITY_PLAN={downstream}'
                )
                line = line.replace('NAME=Automation-Bot', f'NAME={email_name}')
                line = line.replace('EMAIL=automation@example.com', f'EMAIL={email_address}')
                f.write(line)


def update_workflow(workflow_path: pathlib.Path, repo_oscal_type: str, git_owner: str, downstream: str) -> None:
    """Update workflow."""
    with open(workflow_path, 'r') as f:
        lines = f.readlines()
    with open(workflow_path, 'w') as f:
        for line in lines:
            if repo_oscal_type == 'catalog':
                line = line.replace('my-repo-base/my-profile', f'{git_owner}/{downstream}')
                line = line.replace('./my-profile', f'{downstream}')
                f.write(line)
            elif repo_oscal_type == 'profile':
                line = line.replace('my-repo-base/my-component-definition', f'{git_owner}/{downstream}')
                line = line.replace('./my-component-definition', f'{downstream}')
                f.write(line)
            elif repo_oscal_type == 'my-component-definition':
                line = line.replace('my-repo-base/my-system-security-plan', f'{git_owner}/{downstream}')
                line = line.replace('./my-system-security-plan', f'{downstream}')
                f.write(line)


def set_secret(token: str, cwd: str) -> None:
    """Set secret."""
    cmd = f'gh secret set GIT_TOKEN --app actions --body {token}'
    run_cmd(cmd, cwd)


def install_content(repo: Dict, oscal_type: str, cwd: str) -> bool:
    """Install content."""
    rval = False
    content = repo.get('content')
    if not content:
        return rval
    for content_item in content:
        src_folder = content_item.get('src-folder')
        src_file = content_item.get('src-file')
        tgt_folder = content_item.get('tgt-folder')
        tgt_file = content_item.get('tgt-file')
        if not src_file:
            continue
        if not tgt_folder:
            continue
        if src_folder:
            src = pathlib.Path(src_folder) / src_file
        else:
            src = pathlib.Path(src_file)
        if tgt_file:
            tgt = pathlib.Path(tgt_folder) / tgt_file
        else:
            tgt = pathlib.Path(tgt_file) / f'{oscal_type}.json'
        cmd = f'mkdir -p {tgt_folder}'
        run_cmd(cmd, cwd)
        cmd = f'cp -p {src} {tgt}'
        run_cmd(cmd, cwd)
        rval = True
    modify_content(repo, oscal_type, cwd)
    return rval


def modify_content(repo: Dict, oscal_type: str, cwd: str) -> None:
    """Modify content."""
    modify = repo.get('modify')
    if not modify:
        return
    for modify_item in modify:
        tgt_folder = modify_item.get('tgt-folder')
        tgt_file = modify_item.get('tgt-file')
        before = modify_item.get('before')
        after = modify_item.get('after')
        if not tgt_file:
            continue
        if not tgt_folder:
            continue
        p = pathlib.Path(cwd) / tgt_folder / tgt_file
        with open(p, 'r') as f:
            lines = f.readlines()
        with open(p, 'w') as f:
            for line in lines:
                if before in line:
                    line = line.replace(before, after)
                f.write(line)


def run_cmd(cmd: str, cwd: str) -> (str, str):
    """Run command."""
    args = cmd.split()
    if cwd:
        p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # noqa: S603
    else:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # noqa: S603
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    logger.debug(f'cmd: {cmd}')
    logger.debug(f'out: {out}')
    logger.debug(f'err: {err}')
    return (out, err)


def repo_delete(git_scheme: str, git_domain: str, git_owner: str, repo_name: str) -> None:
    """Delete repo."""
    url = synthesize_repo_url(git_scheme, git_domain, git_owner, repo_name)
    cmd = f'gh repo delete {url} --yes'
    _, err = run_cmd(cmd, '')
    if err:
        logger.warning(f'{err}')
    else:
        logger.info(f'repo {url} deleted')


def repo_create(
    git_scheme: str, git_domain: str, git_owner: str, repo_name: str, repo: Dict, email_name: str, email_address: str
) -> None:
    """Create repo."""
    url = synthesize_repo_url(git_scheme, git_domain, git_owner, repo_name)
    repo_oscal_type = repo.get('oscal-type')
    validate_oscal_type(repo_name, repo_oscal_type)
    access = repo.get('access')
    validate_repo_access(access)
    downstream_list = repo.get('downstream')
    if len(downstream_list) > 1:
        logger.warning(f'{repo_name} has > 1 downstream; only 1 supported')
        return
    downstream = downstream_list[0]
    template = repo.get('template')
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = f'gh repo create {url} --{access} --template {template} --clone'
        out, err = run_cmd(cmd, tmpdir)
        if url not in str(out):
            if 'already exists' in str(err):
                logger.warning(f'{url} already exists')
                return
            else:
                raise RuntimeError(err)
        token = os.environ[GH_TOKEN]
        gitdir = f'{tmpdir}/{repo_name}'
        # update repo secret
        set_secret(token, gitdir)
        # update config.env
        config_env_path = pathlib.Path(gitdir) / 'config.env'
        update_config_env(config_env_path, repo_oscal_type, git_owner, repo_name, downstream, email_name, email_address)
        # update main-push.yml
        workflow_path = pathlib.Path(gitdir) / '.github' / 'workflows' / 'main-push.yml'
        update_workflow(workflow_path, repo_oscal_type, git_owner, downstream)
        # remote
        cmd = f'git remote set-url origin https://{git_owner}:{token}@github.com/{git_owner}/{repo_name}.git'
        run_cmd(cmd, gitdir)
        # push repo contents
        cmd = 'git branch -m main'
        run_cmd(cmd, gitdir)
        cmd = 'git add .'
        run_cmd(cmd, gitdir)
        cmd = f'git config user.email {email_address}'
        run_cmd(cmd, gitdir)
        cmd = f'git config user.name {email_name}'
        run_cmd(cmd, gitdir)
        cmd = 'git commit -m Configure'
        run_cmd(cmd, gitdir)
        cmd = 'git push'
        run_cmd(cmd, gitdir)
        # create develop branch
        cmd = 'git branch develop'
        run_cmd(cmd, gitdir)
        cmd = 'git checkout develop'
        run_cmd(cmd, gitdir)
        # install content into develop branch
        if install_content(repo, repo_oscal_type, gitdir):
            cmd = 'git add .'
            run_cmd(cmd, gitdir)
            cmd = f'git config user.email {email_address}'
            run_cmd(cmd, gitdir)
            cmd = f'git config user.name {email_name}'
            run_cmd(cmd, gitdir)
            cmd = 'git commit -m Content'
            run_cmd(cmd, gitdir)
            cmd = 'git push --set-upstream origin develop'
            run_cmd(cmd, gitdir)
    logger.info(f'repo {url} created')


def validate_repo_access(access: str) -> None:
    """Validate access."""
    if not access:
        raise RuntimeError('access missing')
    if access not in ['public', 'private', 'internal']:
        raise RuntimeError(f'access {access} invalid')


class AgAuSetup():
    """Agile Authoring setup."""

    def __init__(self) -> None:
        """Initialize."""

    def run(self) -> None:
        """Run."""
        # parse args
        args = self.parse_args()
        # GH_TOKEN init:
        if args.gh_token:
            os.environ[GH_TOKEN] = args.gh_token
        # validate gh
        validate_gh()
        # read yaml
        ydata = get_yaml(args.config)
        # display version
        version = ydata.get('version')
        logger.debug(f'version: {version}')
        # git info
        git = ydata.get('git')
        git_scheme = git.get('scheme')
        git_domain = git.get('domain')
        git_owner = git.get('owner')
        email = ydata.get('email')
        email_name = email.get('name')
        email_address = email.get('address')
        repos = ydata.get('repos')
        for repo_name in repos:
            repo = repos.get(repo_name)
            if args.action == 'create':
                repo_create(git_scheme, git_domain, git_owner, repo_name, repo, email_name, email_address)
            elif args.action == 'delete':
                repo_delete(git_scheme, git_domain, git_owner, repo_name)
            else:
                raise RuntimeError(f'invalid action {args.action}')

    def parse_args(self) -> Dict:
        """Parse args."""
        description = 'Agile Authoring setup.'
        parser = argparse.ArgumentParser(description=description)
        required = parser.add_argument_group('required arguments')
        #
        help_action = 'one of {create, delete}'
        required.add_argument('--action', action='store', required=True, help=help_action)
        #
        default_config_yaml = 'config.yaml'
        help_config_yaml = f'yaml file containing configuration, default = {default_config_yaml}'
        parser.add_argument('--config', action='store', default=default_config_yaml, help=help_config_yaml)
        #
        default_gh_token = None
        help_gh_token = f'value to be used for {GH_TOKEN}, default = existing environment value of {GH_TOKEN}'
        parser.add_argument('--gh-token', action='store', default=default_gh_token, help=help_gh_token)
        #
        return parser.parse_args()


def main():
    """Mainline."""
    agau_setup = AgAuSetup()
    agau_setup.run()


if __name__ == '__main__':
    main()
