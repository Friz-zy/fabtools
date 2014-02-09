"""
Groups
======
"""
from __future__ import with_statement

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


def exists(name, gid=None):
    """
    Check if a group exists.
    """
    if gid:
        with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
            if gid in run('getent group %(name)s' % locals()).split(":"):
                return True
            return False
    else:
        with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
            return run('getent group %(name)s' % locals()).succeeded


def create(name, gid=None):
    """
    Create a new group.

    Example::

        import fabtools

        if not fabtools.group.exists('admin'):
            fabtools.group.create('admin')

    """

    args = []
    if gid:
        args.append('-g %s' % gid)
    args.append(name)
    args = ' '.join(args)
    run_as_root('groupadd %s' % args)

def modify(name, new_name=None, gid=None):
        """
    Modify a group.

    Example::

        import fabtools

        if fabtools.group.exists('admin'):
            fabtools.group.modify('admin', 'hacker')

    """

    args = []
    if gid:
        args.append('-g %s' % gid)
    if new_name:
        args.append('-n %s' % new_name)
    args.append(name)
    args = ' '.join(args)
    run_as_root('groupmod %s' % args)

def delete(name):
        """
    Delete a group.

    Example::

        import fabtools

        if fabtools.group.exists('admin'):
            fabtools.group.delete('admin')

    """
    run_as_root('groupdel %s' % name)