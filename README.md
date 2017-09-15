A propos
--------

`CondimenStation` is a [salt](https://saltstack.com/)-derived environment to maintain and share
state on personal laptops in an ad-hoc way. It enables users to setup their laptops and dotfiles. It
enables teams to setup separate programming environment for each project and share them. The goal is
to limit the amount of pain when joining a project, while maintaining complete freedom for each user
to do whatever she cares.

Basically, it's github's [boxen](https://github.com/boxen/our-boxen) but chaotic good. With salt
rather than puppet, YAML rather than a homegrown DSL, and python rather than ruby.

Installation
------------

1. Create a directory to hold stuff
1. Inside this main directory clone CondimentStation to subdirectory CondimentStation
1. Fork mdavezac/template_black-garlic and rename your fork to black-garlic
1. Clone your black-garlic to a subdirectory black-garlic inside the main directory
1. Edit the files in pillar/black-garlic to fit your preferences
1. *From the main directory*, run CondimentStation/bootstrap.sh
1. Setup your environment to use spack. My zprofile has:

   ```bash
   export SPACK_ROOT=<spack root>
   source $SPACK_ROOT/share/spack/setup-env.sh

   [[ -e /usr/local/Cellar/lmod/5.9.3/init/zsh ]] && \
     source /usr/local/Cellar/lmod/5.9.3/init/zsh
   module use $HOME/.funwith
   ```

   Where by default `<spack_root>` is `/path/to/main/directory/from/this/readme/build/spack` or
   whatever you've decided on in the pillar `black-garlic/pillar/spack.sls`


Usage
-----

Once installed, you should be able to do:

```bash
module load condiment_station
```

This will setup your environment so you can run states. The states are the `.sls` files found
directly in:

- main_directory/black-garlic
- main_directory/CondimentStation
- main_directory/black-garlic/projects
- main_directory/

Starting with the top-most and falling back to the ones below if a state is not found.

A state can be called with:

```
pinch.py run CondimentStation.projects.condiment_station
```

This will run the state file `CondimentStation/projects/condiment_station.sls`.
Thanks to the fall-back mechanism, we could also just run it with `pinch.py
projects.condiment_station` assuming no such file exist in `black-garlic`.

Any state accessible from `black-garlic/top.sls` will run when `pinch.py run` is called without
argument.

`pinch.py` can also run arbitrary salt modules:

```
pinch.py call pillar.items
```

Or show an state file before running it

```
pinch.py show black-garlic
```

That particular state is a staple from the black-garlic template. It simply inherits from the state
in `CondimentStation/projects/condiment_station`. Do look inside
`black-garlic/projects/black-garlic.sls` to figure out add your own stuff to somebody-elses project.


Adding other peoples projects
-----------------------------

The pillar `black-garlic/pillar/condiments` make it easy to add other peoples dotfiles/projects and
include them in your own.

Assuming it contains:

```YAML
condiments:
   chilly-oil:
       github: mdavezac/black-garlic
```

Then running:

```bash
pinch.py run condiments
```

Will download mdavezac's black-garlic into the `chilly-oil` subdirectory of the main directory. From
there, it can be used directly by running `pinch.py run chilly-oil.some_state` or by
including states in your own black-garlic.

Exemplar project file
---------------------

```YAML
{% set compiler = salt["spack.compiler"]() %}
{% set python = salt['pillar.get']('python', 'python3') %}
{% set mpilib = salt['pillar.get']('mpi', 'openmpi') %}
{% set project = sls.split('.')[-1] %}
{% set workspace = salt['funwith.workspace'](project) %}

{{project}} spack packages:
  spack.installed:
    - pkgs: &spack_packages
      - GreatCMakeCookoff
      - eigen %{{compiler}} -fftw -scotch -metis -suitesparse
      - swig %{{compiler}}

{{workspace}}/{{python}}:
  virtualenv.managed:
    - python: {{python}}
    - pip_upgrade: True
    - use_wheel: True
    - pip_pkgs: [pip, numpy, scipy, pytest, pandas, cython, behave]

DCPROGS/HJCFIT:
  github.latest:
    - target: {{workspace}}/src/{{project}}

dcprogs:
  funwith.modulefile:
    - spack: *spack_packages
    - virtualenv: {{workspace}}/{{python}}
{% if compiler == "gcc" %}
    - footer: |
        setenv("CXX", "g++-6")
        setenv("CC", "gcc-6")
{% endif %}
```

There are few variables of interest here:

- compiler: specifies the spack compiler collection to use. It can be modified from the command-line
with `pinch.py run --compiler clang`
- python: either `python2` or `python3` and can also be modified from the command-line.
- project: the name of the current sls file, for convenience
- workspace: a project-specific location where the projects can go.

Running the file above will create a virtualenv in the specific workspace directory, add some spack
packages, download the sources for the program of interest, and add a module file to setup the
enviroment.

After running this particular project, it should be possible to do:

```bash
module load dcprogs
```

And the dcprogs environment will be setup so the right spack libraries are found, the virtualenv is
activated, etc...

Configuration
-------------

All configuration should happen in files in the pillar subdirectory of your black-garlic.  These
file need to be included in `black-garlic/pillar/top.sls` for salt to register them.

black-garlic/pillar/secrets.sls:
    Never commited to version control. This is where secrets should go.

workspaces:
  A directory where all project workspaces will go.

modulefiles:
  A directory where all project module files will go. This directory should be loaded by lmod,
  `module use <directory>`, somewhere in your  `.bash_profile`.

spack:compilers_file:
  Points to a file defining spack-compilers. See spack itself for a description. Optional.

spack:external_packages:
  Points to a file defining the equivalent of spack-packages installed some other way (brew?). See
  spack for description.

spack:directory:
  Where the main spack repo will go

spack:repo_prefix:
  Where subsidiary repos of spack-packages are installed.

spack:repos:
  Dictionary with subsidiary spack repos.


The following configuration is generated by `CondimentStation/bin/bootstrap.sh` into
`black-garlic/pillar/salt.sls` and should not be messed with:

user:
    User using condiment station

condiment_prefix:
    Main directory for condiment station

condiment_dir:
    Directory containing CondimentStation itself

condiment_python:
    Executable with to the python executable for the virtualenv used by condiment station

condiment_build_dir:
    Directory with most files generated by CondimentStation. This directory can be removed and then regenerated with `CondimentStation/bin/bootstrap.sh`
