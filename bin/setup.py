#! /usr/bin/env python
import click
from os.path import dirname
from os import getcwd
condiment_dir=dirname(dirname(__file__))
default_prefix=dirname(condiment_dir)

@click.group(help="Setup functions for condiment station")
def cli():
    pass

@cli.command(help="link modules and friends to prefix")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
def server_hierarchy(prefix):
    from py.path import local
    srv = local(prefix).join('build', 'srv', 'salt')
    srv.ensure(dir=True)
    srv.join('_states').mksymlinkto(local(condiment_dir).join('_states'))
    srv.join('_modules').mksymlinkto(local(condiment_dir).join('_modules'))
    srv.join('_grains').mksymlinkto(local(condiment_dir).join('_grains'))

    local(prefix).join('build', 'etc', 'salt').ensure(dir=True)
    local(prefix).join('build', 'var', 'log', 'salt').ensure(dir=True)
    local(prefix).join('build', 'var', 'cache', 'salt', 'master').ensure(dir=True)


@cli.command(help="Overwrites default salt paths")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
def syspath(prefix):
    from py.path import local
    from salt import __file__ as saltfile
    local(local(saltfile).dirname).join("_syspaths.py").write(
        'ROOT_DIR="{prefix}/build"\n'
        'CONFIG_DIR=None\n'
        'CACHE_DIR=None\n'
        'SOCK_DIR=None\n'
        'SRV_ROOT_DIR=None\n'
        'BASE_FILE_ROOTS_DIR=None\n'
        'BASE_PILLAR_ROOTS_DIR=None\n'
        'BASE_MASTER_ROOTS_DIR=None\n'
        'LOGS_DIR=None\n'
        'PIDFILE_DIR=None\n'
        'SPM_FORMULA_PATH=None\n'
        'SPM_PILLAR_PATH=None\n'
        'SPM_REACTOR_PATH=None\n'
        'BASE_THORIUM_ROOTS_DIR=None'.format(prefix=prefix)
    )

@cli.command(help="Adds minion configuration file")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
@click.option('--user', envvar='USER', help="Default user")
@click.option('--sudo_user', envvar='USER', help="Default sudo user")
def minion(prefix, user, sudo_user):
    from py.path import local
    local(prefix).join('build', 'etc', 'salt', 'minion').write(
       'file_client: local\n'
       'user: {user}\n'
       'sudo_user: {sudo_user}\n'
       'pkg: brew\n'
       'file_roots:\n'
       '  base:\n'
       '    - {prefix}/black-garlic\n'
       '    - {prefix}\n'
       '    - {condiment}\n'.format(
           prefix=prefix, condiment=condiment_dir, user=user, sudo_user=sudo_user)
    )

@cli.command(help="Add pillar with condiment station stuff")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
@click.option('--user', envvar='USER', help="Default user")
def pillar(prefix, user):
    from py.path import local
    local(prefix).join('pillar').ensure(dir=True)
    local(prefix).join('pillar', 'secrets.sls').ensure(file=True)
    local(prefix).join('pillar', 'condiment.sls').write(
        'user: {user}\n'
        'condiment_dir: {condiment}\n'
        'condiment_build_dir: {prefix}/build\n'.format(
            condiment=condiment_dir, user=user, prefix=prefix)
    )


@cli.command(help="Add main repo")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
@click.option('--repo', required=True, nargs=1)
@click.option('--branch', default="master", nargs=1)
@click.option('--subdir', default="black-garlic", nargs=1)
def blackgarlic(prefix, repo, branch, subdir):
    from py.path import local
    from git import Repo
    Repo.clone_from(repo, str(local(prefix).join('black-garlic')), branch=branch)

if __name__ == '__main__':
    cli()
