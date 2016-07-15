#! /usr/bin/env python
from py.path import local
import click
import setup

default_prefix = setup.default_prefix


def _options(prefix=default_prefix):
    from py.path import local
    return str(local(prefix).join('build', 'etc', 'salt', 'minion'))


@click.group()
def cli():
    pass

cli.add_command(setup.cli, 'setup')


@cli.command(help="Run a given state, or all states if none given")
@click.option('--prefix', default=default_prefix, type=click.Path(), nargs=1)
@click.argument('states', nargs=-1)
def run(prefix, states):
    setup.run_command(prefix, 'state.apply', *states)


@cli.command(help="Make a call to salt")
@click.argument('call', nargs=-1)
@click.option('--prefix', default=default_prefix, type=click.Path())
def call(prefix, call):
    assert len(call) >= 1
    setup.run_command(prefix, *call)


@cli.command(help="Show a (the) given state(s) in yaml format")
@click.argument('states', nargs=-1)
@click.option('--prefix', default=default_prefix, type=click.Path())
def show(states, prefix):
    setup.run_command(prefix, 'state.show_sls', *states)

if __name__ == '__main__':
    cli()
