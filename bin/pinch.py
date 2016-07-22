#! {{condiment_python}}
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


def _get_compiler(prefix, compiler):
    if compiler is not None and len(compiler) > 0:
        return compiler
    result = setup.get_pillar(prefix, 'compiler')['compiler']
    if len(result) > 0:
        return result
    return "gcc"


def _get_python(prefix, python):
    if python is not None and len(python) > 0:
        return python
    result = setup.get_pillar(prefix, 'python')['python']
    if len(result) > 0:
        return result
    return "python2"


def _get_pillar(prefix, compiler, python):
    return {'compiler': _get_compiler(prefix, compiler),
            'python': _get_python(prefix, python)}


@cli.command(help="Run a given state, or all states if none given")
@click.option('--prefix', default=default_prefix, type=click.Path(), nargs=1)
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
@click.argument('states', nargs=-1)
def run(prefix, states, python, compiler):
    pillars = _get_pillar(prefix, compiler, python)
    setup.run_command(prefix, 'state.apply', *states, pillar=pillars, minimize=True)


@cli.command(help="Make a call to salt")
@click.argument('call', nargs=-1)
@click.option('--prefix', default=default_prefix, type=click.Path())
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
def call(prefix, call, python, compiler):
    assert len(call) >= 1
    pillars = _get_pillar(prefix, compiler, python)
    setup.run_command(prefix, *call, pillar=pillars, minimize=False)


@cli.command(help="Show a (the) given state(s) in yaml format")
@click.argument('states', nargs=-1)
@click.option('--prefix', default=default_prefix, type=click.Path())
@click.option('--compiler', default=None, type=str, nargs=1,
              help="Compiler collection for spack modules")
@click.option('--python', default=None, type=str, nargs=1,
              help="Default python")
def show(states, prefix, compiler, python):
    pillars = _get_pillar(prefix, compiler, python)
    setup.run_command(prefix, 'state.show_sls', *states, pillar=pillars, minimize=False)

if __name__ == '__main__':
    cli()
