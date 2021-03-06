#!/usr/bin/env python
"""Find repos with no openedx.yaml file."""

from __future__ import print_function

import itertools

import click
from edx_repo_tools.auth import pass_github
from edx_repo_tools.data import pass_repo_tools_data, iter_nonforks
from edx_repo_tools.utils import dry_echo, dry


@click.command()
@pass_github
@pass_repo_tools_data
@click.option('--org', multiple=True, default=['edx', 'edx-ops'])
@dry
def no_yaml(hub, repo_tools_data, org, dry):
    """Find public repos with no openedx.yaml file."""
    repos = iter_nonforks(hub, org)
    repos = sorted(repos, reverse=True, key=lambda r: r.pushed_at)
    for repo in repos:
        if repo.private:
            continue
        contents = repo.contents('openedx.yaml')
        if contents is None:
            print("{}: {:%Y-%m-%d}".format(repo.full_name, repo.pushed_at))
            try:
                commits = list(itertools.islice(repo.iter_commits(), 5))
            except Exception as exc:
                print("  Error: {}".format(exc))
                continue
            for commit in commits:
                commit.refresh()
                # last_modified is a string?? 'Fri, 06 Apr 2018 19:48:42 GMT'
                when = " ".join(commit.last_modified.split()[1:4])
                message = commit.commit.message.splitlines()[0]
                print("  {}: {} ({})".format(commit.author, message, when))
