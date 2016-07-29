# -*- coding: utf-8 -*-
'''
Homebrew Cask for Mac OS X
'''
from __future__ import absolute_import

# Import python libs
import copy
import logging

# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError, MinionError

log = logging.getLogger(__name__)

from salt.modules import mac_brew


def _call_cask(cmd):
    '''
    Calls the brew command with the user account of brew
    '''
    mac_brew.__salt__ = __salt__
    mac_brew.__opts__ = __opts__
    return mac_brew._call_brew(cmd)

def list_pkgs(check_context=True, **kwargs):
    '''
    List the packages currently installed in a dict::

        {'<package_name>': '<version>'}

    CLI Example:

    .. code-block:: bash

        salt '*' cask.list_pkgs
    '''
    # not yet implemented or not applicable
    if any([salt.utils.is_true(kwargs.get(x))
            for x in ('removed', 'purge_desired')]):
        return {}

    if check_context and 'cask.list_pkgs' in __context__:
      ret = copy.deepcopy(__context__['cask.list_pkgs'])
      __salt__['pkg_resource.stringify'](ret)
      return ret

    cmd = 'brew cask list'
    ret = {}
    out = _call_cask(cmd)['stdout']
    for line in out.splitlines():
        name_and_versions = line.split(' ')
        name = name_and_versions[0]
        is_installed = _call_cask('brew cask info ' + name)['stdout']
        if 'Not installed' not in is_installed:
            __salt__['pkg_resource.add_pkg'](ret, name, 'present')

    __salt__['pkg_resource.sort_pkglist'](ret)
    __context__['cask.list_pkgs'] = copy.deepcopy(ret)
    __salt__['pkg_resource.stringify'](ret)
    return ret


def install(name=None, pkgs=None, options=None, **kwargs):
    '''
    Install the passed package(s) with ``brew install``

    name
        The name of the formula to be installed. Note that this parameter is
        ignored if "pkgs" is passed.

        CLI Example:

        .. code-block:: bash

            salt '*' cask.install <package name>

    options
        Options to pass to brew. Only applies to initial install. Due to how brew
        works, modifying chosen options requires a full uninstall followed by a
        fresh install. Note that if "pkgs" is used, all options will be passed
        to all packages. Unrecognized options for a package will be silently
        ignored by brew.

        CLI Example:

        .. code-block:: bash

            salt '*' cask.install <package name> tap='<tap>'
            salt '*' cask.install php54 taps='["josegonzalez/php", "homebrew/dupes"]' options='["--with-fpm"]'

    Multiple Package Installation Options:

    pkgs
        A list of formulas to install. Must be passed as a python list.

        CLI Example:

        .. code-block:: bash

            salt '*' cask.install pkgs='["foo","bar"]'


    Returns a dict containing the new package names and versions::

        {'<package>': {'old': '<old-version>',
                       'new': '<new-version>'}}

    CLI Example:

    .. code-block:: bash

        salt '*' cask.install 'package package package'
    '''
    try:
        pkg_params, pkg_type = __salt__['pkg_resource.parse_targets'](
            name, pkgs, kwargs.get('sources', {})
        )
    except MinionError as exc:
        raise CommandExecutionError(exc)

    if pkg_params is None or len(pkg_params) == 0:
        return {}

    formulas = ' '.join(pkg_params)
    old = list_pkgs()

    # Ensure we've tapped the repo if necessary
    if options:
        cmd = 'brew cask install {0} {1}'.format(formulas, ' '.join(options))
    else:
        cmd = 'brew cask install {0}'.format(formulas)

    _call_cask(cmd)

    new = list_pkgs(check_context=False)
    return salt.utils.compare_dicts(old, new)
