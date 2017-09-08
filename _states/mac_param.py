import salt.utils


def modify(name, domain, **params):
    if len(params) == 0:
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': 'No new profiles, and no params'}
    changes = {}
    for key, value in params.items():
        old = __salt__['mac_params.get_param'](key, domain=domain)
        if old != str(value):
            changes[key] = {'old': old, 'new': value}

    if len(changes) == 0:
        return {'name': name,
                'changes': {},
                'result': None,
                'comment': 'No changes'}
    if __opts__['test']:
        return {'name': name,
                'changes': changes,
                'result': None,
                'comment': name + ' keys: ' + str(changes.keys())}
    for key, value in changes.items():
        __salt__['mac_params.set_param'](key, value['new'], domain=domain)

    return {'name': name,
            'changes': changes,
            'result': True,
            'comment': 'following changes: ' + str(changes)}
