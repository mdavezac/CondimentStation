def _create_package_name(name, version=None, options=None, compiler=None):
    result = name
    if version:
        result += "@" + version
    if isinstance(options, str):
        result += " " + options
    elif options is not None:
        result += " " + " ".join(options)
    if compiler is not None:
        result += " %" + compiler
    return result


def installed(name, pkgs=None, environ=None, compiler=None, **kwargs):
    from os.path import join
    defaults = __salt__['spack.defaults']()
    if isinstance(pkgs, list) and len(pkgs) == 0:
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': 'No packages to install provided'}
    if not (isinstance(pkgs, list) and len(pkgs) != 0):
        pkgs = [name]

    new_pkgs = [p for p in pkgs if not __salt__['spack.is_installed'](p, compiler=compiler)]
    if len(new_pkgs) == 0:
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': 'All modules already installed'}
    if __opts__['test']:
       changes = {pkg: '' for pkg in new_pkgs}
       return {'name': name,
               'changes': changes,
               'result': None,
               'comment': 'Spacking ' + str(new_pkgs)}

    changes = {}
    result = True
    for pkg in new_pkgs:
      installed, failed = __salt__['spack.install'](
          pkg, environs=environ, compiler=compiler, **kwargs)
      result &= len(failed) == 0
      changes.update({p: {'old': None, 'new': 'installed'} for p in installed})
    return {'name': name,
            'changes': changes,
            'result': result,
            'comment': 'Installed new packages'}


def add_repo(name, github=None, scope=None, prefix=None):
    from os.path import expanduser, join

    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}
    target = __salt__['spack.repo_path'](name)

    if github is not None:
        spackdir = __salt__['spack.spack_directory']()
        __states__['github.latest'](name=github, target=target)

    if __salt__['spack.repo_exists'](target):
        ret['result'] = True
        ret['comment'] = 'System already in the correct state'
        return ret

    ret['changes'] = {
        'old': 'repo not found',
        'new': '%s installed at %s' % (
            name if github is None else github, target)
    }
    if __opts__['test'] == True:
        ret['comment'] = 'The state of "{0}" will be changed.'.format(name)
        ret['result'] = None
        return ret

    __salt__['spack.add_repo'](target)
    ret['comment'] = 'Spack repo "{0}" installed.'.format(name)
    ret['result'] = True
    return ret
