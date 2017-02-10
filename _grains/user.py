def _shell():
    from os import environ
    return {'shell': environ['SHELL']}


def _user():
    from getpass import getuser
    return {'user': getuser()}


def _home():
    from getpass import getuser
    from os.path import expanduser
    return {'userhome': expanduser("~" + getuser())}


def _pythons(prefix="/usr/local/Cellar"):
    from glob import glob
    from os.path import join, dirname
    from packaging.version import parse
    from re import search
    result = {}
    paths = join(prefix, "python*", "[0-9].[0-9].[0-9]*", "Frameworks",
                 "Python.framework", "Versions", "[0-9].[0-9]", "bin",
                 "python[2-3]")
    for path in glob(join(paths)):
        v = search(r"\/(\d\.\d\.\d+)(?:_\d+)?\/", path).group(1)
        result["python@" + v] = path

    python2 = max([u for u in result.keys() if parse(u)
                   < parse("3.0.0")], key=parse)
    python3 = max(result.keys(), key=parse)
    return {"python2": result[python2],
            "python3": result[python3],
            "pythons": result}


def _programs(program, bin=None, prefix="/usr/local/Cellar"):
    from glob import glob
    from os.path import join, dirname
    from packaging.version import parse
    from re import search
    if bin is None:
        bin = program

    result = {}
    paths = join(prefix, program, "[0-9].[0-9].[0-9]*", "bin", bin)
    for path in glob(join(paths)):
        v = search(r"\/(\d\.\d\.\d+)(?:_\d+)?\/", path).group(1)
        result[program + "@" + v] = path

    return {program + "s": result}


def _mac_version():
    from packaging.version import parse
    from platform import mac_ver
    ver = parse(mac_ver()[0])

    if parse("10.13") > ver >= parse("10.12"):
        return {"mac_version": "sierra"}
    if parse("10.12") > ver >= parse("10.11"):
        return {"mac_version": "elcapitan"}


def _gccs(prefix="/usr/local/Cellar"):
    from glob import glob
    from os.path import join, dirname
    from packaging.version import parse
    from re import search

    result = {}
    paths = join(prefix, "gcc*", "[0-9].[0-9].[0-9]*", "bin")
    possibles = {"cc": "gcc-[0-9]*", "cxx": "g++-*",
                 "f77": "gfortran-*", "fc": "gfortran-*"}
    for path in glob(join(paths)):
        v = search(r"\/(\d\.\d\.\d+)(?:_\d+)?\/", path).group(1)
        compilers = {}

        for comp, name in possibles.iteritems():
            if len(glob(join(path, name))):
                compilers[comp] = glob(join(path, name))[-1]

        result["gcc@" + v] = compilers

    return {"gccs": result}


def main():
    grains = {}
    grains.update(_user())
    grains.update(_shell())
    grains.update(_home())
    grains.update(_pythons())
    grains.update(_programs("cmake"))
    grains.update(_programs("git"))
    grains.update(_programs("pcre", "pcregrep"))
    grains.update(_mac_version())
    grains.update(_gccs())
    return grains
