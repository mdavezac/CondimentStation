#! /usr/bin/env python
import click
from os.path import dirname
condiment_dir = dirname(dirname(__file__))
default_prefix = dirname(condiment_dir)


def _options(prefix):
    from py.path import local
    return str(local(prefix).join('build', 'etc', 'salt', 'minion'))


@click.group(help="Setup functions for condiment station")
def cli():
    pass


def run_command(prefix, command, *states):
    import salt.client
    import salt.output.yaml_out
    import salt.config
    __opts__ = salt.config.minion_config(str(_options(prefix)))
    __opts__['file_client'] = 'local'
    # makes it possible to use password-protected ssh identity files
    __opts__['__cli'] = ('salt-call', )
    caller = salt.client.Caller(mopts=__opts__)
    output = salt.output.yaml_out
    output.__opts__ = __opts__
    if len(states) == 0:
        print(output.output(caller.cmd(command)))
    else:
        for state in states:
            print(output.output(caller.cmd(command, state)))


@cli.command(help="link modules and friends to prefix")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
def server_hierarchy(prefix):
    from py.path import local
    srv = local(prefix).join('build', 'srv', 'salt')
    srv.ensure(dir=True)
    if not srv.join('_states').exists():
        srv.join('_states').mksymlinkto(local(condiment_dir).join('_states'))
    if not srv.join('_modules').exists():
        srv.join('_modules').mksymlinkto(local(condiment_dir).join('_modules'))
    if not srv.join('_grains').exists():
        srv.join('_grains').mksymlinkto(local(condiment_dir).join('_grains'))

    local(prefix).join('build', 'etc', 'salt').ensure(dir=True)
    local(prefix).join('build', 'var', 'log', 'salt').ensure(dir=True)
    local(prefix).join('build', 'var', 'cache', 'salt', 'master').ensure(dir=True)


@cli.command(help="Overwrites default salt paths")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
def syspath(prefix):
    from py.path import local
    from salt import __file__ as saltfile
    local(local(saltfile).dirname).join("_syspaths.py").write(
        'ROOT_DIR="{prefix}"\n'
        'CONFIG_DIR="{prefix}/build/etc/salt"\n'
        'CACHE_DIR="{prefix}/build/var/cache/salt"\n'
        'SOCK_DIR="{prefix}/build/var/run/salt"\n'
        'SRV_ROOT_DIR="{prefix}/build/srv"\n'
        'BASE_FILE_ROOTS_DIR=None\n'
        'BASE_PILLAR_ROOTS_DIR=None\n'
        'BASE_MASTER_ROOTS_DIR=None\n'
        'LOGS_DIR="{prefix}/build/var/log/salt"\n'
        'PIDFILE_DIR="{prefix}/build/var/run"\n'
        'SPM_FORMULA_PATH="{prefix}/build/spm/salt"\n'
        'SPM_PILLAR_PATH="{prefix}/build/spm/pillar"\n'
        'SPM_REACTOR_PATH="{prefix}/build/spm/reactor"\n'
        'BASE_THORIUM_ROOTS_DIR=None'.format(prefix=prefix)
    )


@cli.command(help="Adds minion configuration file")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
@click.option('--user', envvar='USER', help="Default user")
@click.option('--sudo_user', envvar='USER', help="Default sudo user")
def minion(prefix, user, sudo_user):
    from py.path import local
    etc = local(prefix).join('build', 'etc', 'salt')
    etc.join('master').write(
        'file_client: local\n'
        'user: {user}\n'
        'sudo_user: {sudo_user}\n'
        'pkg: brew\n'
        'pillar_roots:\n'
        '  base:\n'
        '    - {prefix}/black-garlic/pillar\n'
        'file_roots:\n'
        '  base:\n'
        '    - {prefix}/black-garlic\n'
        '    - {prefix}/CondimentStation\n'
        '    - {prefix}/black-garlic/projects\n'.format(
            prefix=prefix, user=user, sudo_user=sudo_user)
    )
    if not etc.join('minion').exists():
        etc.join('minion').mksymlinkto(etc.join('master'))


@cli.command(help="Add pillar with condiment station stuff")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
@click.option('--user', envvar='USER', help="Default user")
def pillar(prefix, user):
    from py.path import local
    directory = local(prefix).join('black-garlic', 'pillar')
    directory.ensure(dir=True)
    directory.join('secrets.sls').ensure(file=True)
    directory.join('salt.sls').write(
        'user: {user}\n'
        'condiment_prefix: {prefix}\n'
        'condiment_dir: {condiment}\n'
        'condiment_build_dir: {prefix}/build\n'.format(
            condiment=condiment_dir, user=user, prefix=prefix)
    )


@cli.command(help="Add main repo")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
@click.option('--repo', required=True, nargs=1)
@click.option('--branch', default="master", nargs=1)
@click.option('--subdir', default="black-garlic", nargs=1)
def blackgarlic(prefix, repo, branch, subdir):
    from py.path import local
    from git import Repo
    Repo.clone_from(repo, str(local(prefix).join('black-garlic')), branch=branch)


@cli.command(help="Runs bootstrap states")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
def initial_states(prefix):
    run_command(prefix, "state.sls", 'brew-cask', 'salt')


@cli.command(help="Sync states and modules")
@click.argument('prefix', default=default_prefix, type=click.Path(), nargs=1)
def sync(prefix):
    run_command(prefix, 'saltutil.sync_all')


if __name__ == '__main__':
    cli()
