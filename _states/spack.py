def _get_spack(pillars=None):
    from os.path import join, expanduser
    if pillars is None:
        pillars = __pillar__
    if 'spack' not in pillars:
        return {
          'directory': __grains__['userhome'] + "/spack",
          'config_dir': __grains__['userhome'] + ".spack",
          'compiler': 'clang@7.0.3'
        }
    return pillars['spack']

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

def installed(name, compiler=None, options=None, version=None, dependencies=None,
          **kwargs):
    from os.path import join
    defaults = _get_spack(__pillar__)
    specs = _create_package_name(
        name, version=version, options=options, compiler=compiler)
    if isinstance(dependencies, str):
        specs += " " + dependencies
    elif isinstance(dependencies, list):
        specs += " " + " ".join(dependencies)
    elif dependencies is not None:
        for package in dependencies:
            specs += _create_package_name(**package)
    spacker = join(defaults['directory'], 'bin', 'spack')
    return __states__['cmd.run'](spacker + " install " + specs)

def recipe(name, file=None):
    from os.path import join
    defaults = _get_spack(__pillar__)
    prefix = join(defaults['directory'], 'var', 'spack', 'packages', name)
    source = 'salt://spack/' + (name if file is None else file)
    results = {}
    results.update(__states__['file.directory'](prefix))
    results.update(
        __states__['file.managed'](join(prefix, 'package.py'), source=source))
    return results

def add_repo(name, github=None):
    from os.path import expanduser, join

    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}
    if github is not None:
        spackdir = __salt__['pillar.get']('spack:directory', expanduser(join("~", "spack")))
        target = join(spackdir, 'var', 'repos', name)
        gitresults = __states__['github.latest'](name=github, target=target)
    else:
        gitresults = {}
        target = name

    if __salt__['spack.repo_exists'](target):
        ret['result'] = True
        ret['comment'] = 'System already in the correct state'
        return ret

    ret['changes'] = {
        'old': 'repo not found',
        'new': 'repo installed'
    }
    if __opts__['test'] == True:
        ret['comment'] = 'The state of "{0}" will be changed.'.format(name)

        # Return ``None`` when running with ``test=true``.
        ret['result'] = None

        return ret

    __salt__['spack.add_repo'](target)
    ret['comment'] = 'Spack repo "{0}" installed.'.format(name)
    ret['result'] = True
    return ret
