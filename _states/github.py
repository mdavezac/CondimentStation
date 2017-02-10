import salt.utils
from os.path import splitext, split

gitname = splitext(split(__file__)[1])[0]


def _config_set(repo, email=None, username=None):
    result = {}
    if email is not None:
        result.update(__states__['git.config_set'](
            repo=repo, name='user.email', value=email))
    if username is not None:
        result.update(__states__['git.config_set'](
            repo=repo, name='user.name', value=username))

    return result


def _call(module, name, **kwargs):
    from os.path import exists, join, expanduser
    from getpass import getuser
    name = "git@{0}.com:{1}".format(gitname, name)
    user = kwargs.get('user', getuser())
    identity = expanduser("~{0}/.ssh/{1}_rsa".format(gitname, user))
    if 'identity' not in kwargs and exists(identity):
        kwargs['identity'] = identity
    return module(name, **kwargs)


def latest(name, target=None, email=None, username=None, **kwargs):
    """ Sets up github repo """
    # Make sure we set up tracking
    result = _call(__states__['git.latest'], name, target=target, **kwargs)
    if target is not None:
        result.update(_config_set(target, email=email, username=username))
    return result
latest.__doc__ = latest.__doc__.replace("github", gitname)
