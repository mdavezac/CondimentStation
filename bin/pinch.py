#! /usr/bin/env python
from os import getcwd
import click
import setup


@click.group()
def cli():
    pass

cli.add_command(setup.cli, 'setup')

@cli.command(help="Sync states and modules")
@click.argument('prefix', default=getcwd(), type=click.Path(), nargs=1)
def sync(prefix):
    from py.path import local
    import salt.client
    import salt.config
    __opts__ = salt.config.minion_config(str(local(prefix).join('etc', 'minion')))
    __opts__['file_client'] = 'local'
    caller = salt.client.Caller(mopts=__opts__)
    caller.cmd('saltutil.sync_all')


if __name__ == '__main__':
    cli()
