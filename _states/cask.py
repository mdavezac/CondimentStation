from __future__ import absolute_import
import salt.utils


def installed(
        name,
        refresh=None,
        pkgs=None,
        **kwargs):
    '''
    Ensure that the package is installed, and that it is the correct version
    (if specified).

    :param str name:
        The name of the package to be installed. This parameter is ignored if
        "pkgs" is used. Additionally, please note that this
        option can only be used to install packages from a software repository.
        To install a package file manually, use the "sources" option detailed
        below.

    :param bool refresh:
        Update the repo database of available packages prior to installing the
        requested package.

    :param list pkgs:
        A list of packages to install from a software repository. All packages
        listed under ``pkgs`` will be installed via a single command.

        Example:

        .. code-block:: yaml

            mypkgs:
              pkg.installed:
                - pkgs:
                  - foo
                  - bar
                  - baz
                - hold: True

        ``NOTE:`` For :mod:`apt <salt.modules.aptpkg>`,
        :mod:`ebuild <salt.modules.ebuild>`,
        :mod:`pacman <salt.modules.pacman>`,
        :mod:`yumpkg <salt.modules.yumpkg>`,
        and :mod:`zypper <salt.modules.zypper>`,
        version numbers can be specified
        in the ``pkgs`` argument. For example:

        .. code-block:: yaml

            mypkgs:
              pkg.installed:
                - pkgs:
                  - foo
                  - bar: 1.2.3-4
                  - baz

        Additionally, :mod:`ebuild <salt.modules.ebuild>`,
        :mod:`pacman <salt.modules.pacman>` and
        :mod:`zypper <salt.modules.zypper>` support the ``<``, ``<=``, ``>=``,
        and ``>`` operators for more control over what versions will be
        installed. For

        Example:

        .. code-block:: yaml

            mypkgs:
              pkg.installed:
                - pkgs:
                  - foo
                  - bar: '>=1.2.3-4'
                  - baz

        ``NOTE:`` When using comparison operators, the expression must be
        enclosed in quotes to avoid a YAML render error.

        With :mod:`ebuild <salt.modules.ebuild>` is also possible to specify a
        use flag list and/or if the given packages should be in
        package.accept_keywords file and/or the overlay from which you want the
        package to be installed.

        For example:

        .. code-block:: yaml

            mypkgs:
              pkg.installed:
                - pkgs:
                  - foo: '~'
                  - bar: '~>=1.2:slot::overlay[use,-otheruse]'
                  - baz

        **Multiple Package Installation Options: (not supported in Windows or
        pkgng)**

    :return:
        A dictionary containing the state of the software installation
    :rtype dict:

    '''
    if isinstance(pkgs, list) and len(pkgs) == 0:
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': 'No packages to install provided'}
    if not (isinstance(pkgs, list) and len(pkgs) != 0):
        pkgs = [name]

    current = __salt__['cask.list_pkgs']()
    new_pkgs = [u for u in pkgs if u not in current]
    if len(new_pkgs) == 0:
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': 'All packages already installed'}
    if __opts__['test']:
        changes = {pkg: '' for pkg in new_pkgs}
        return {'name': name,
                'changes': changes,
                'result': None,
                'comment': 'Casking ' + str(new_pkgs)}
    changes = __salt__['cask.install'](pkgs=new_pkgs, **kwargs)
    result = set(changes.keys()) == set(new_pkgs)
    return {'name': name,
            'changes': changes,
            'result': result,
            'comment': 'Installed new packages'}
