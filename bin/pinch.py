#! /usr/bin/env python
from os import getcwd
import click
import setup


@click.group()
def cli():
    pass

cli.add_command(setup.cli, 'setup')

def _options(prefix):
    from py.path import local
    return str(local(prefix).join('build', 'etc', 'salt', 'minion'))

@cli.command(help="Sync states and modules")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
def sync(prefix):
    import salt.client
    import salt.config
    __opts__ = salt.config.minion_config(str(_options(prefix)))
    __opts__['file_client'] = 'local'
    caller = salt.client.Caller(mopts=__opts__)
    print(caller.cmd('saltutil.sync_all'))

@cli.command(help="Make a call to salt")
@click.argument('call', nargs=-1)
@click.option('--prefix', default=getcwd(), type=click.Path())
def call(call, prefix):
    import salt.client
    import salt.config
    __opts__ = salt.config.minion_config(str(_options(prefix)))
    __opts__['file_client'] = 'local'
    caller = salt.client.Caller(mopts=__opts__)
    print(caller.cmd(*call))

if __name__ == '__main__':
    cli()
