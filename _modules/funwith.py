def defaults(key=None, value=None):
    """ Default pillar values """
    from os.path import join
    if key is not None and value is not None:
        return value
    home = __grains__['userhome']
    lmodfiles = join(home, '.funwith')
    workspaces = join(home, 'workspaces')
    values = {
        'workspaces': __salt__['pillar.get']('funwith:workspaces', workspaces),
        'modulefiles':
            __salt__['pillar.get']('funwith:modulefiles', lmodfiles),
    }
    return values[key] if key is not None else values


def workspace(name):
    """ Computes workspace prefix for given project """
    from os.path import join
    return join(defaults('workspaces'), name)
