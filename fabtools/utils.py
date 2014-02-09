"""
Utilities
=========
"""
from __future__ import with_statement

import os
import posixpath

from fabric.api import env, hide, run, sudo


def run_as_root(command, *args, **kwargs):
    """
    Run a remote command as the root user.

    When connecting as root to the remote system, this will use Fabric's
    ``run`` function. In other cases, it will use ``sudo``.
    """
    if env.user == 'root':
        func = run
    else:
        func = sudo
    return func(command, *args, **kwargs)


def get_cwd(local=False):

    from fabric.api import local as local_run

    with hide('running', 'stdout'):
        if local:
            return local_run('pwd', capture=True)
        else:
            return run('pwd')


def abspath(path, local=False):

    path_mod = os.path if local else posixpath

    if not path_mod.isabs(path):
        cwd = get_cwd(local=local)
        path = path_mod.join(cwd, path)

    return path_mod.normpath(path)

def find_utility(name, use_sudo=False):
    """
    Return path to the utility
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        utility = func(u'which %s' % name)
        if utility and exists(utility):
            return utility
        elif func(utility).succeeded:
            return name
        else:
            abort('No "%s" utility was found on this system.' % name)