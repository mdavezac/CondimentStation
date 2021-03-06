{% set directory = salt['spack.defaults']('directory') %}
{% set config_dir = salt['spack.defaults']('config_dir') %}
spack:
  github.latest:
    - order: 0
    - target: {{directory}}
    - name: llnl/spack.git
    - rev: develop
    - force_fetch: True

{% set spack = salt['pillar.get']('spack', {}) %}
{% if spack.get('add_to_zprofile', False) %}
spack zprofile:
  file.append:
    - name: {{grains['userhome']}}/.salted/zprofile
    - text: |
       export SPACK_ROOT={{directory}}
       source $SPACK_ROOT/share/spack/setup-env.sh
{% endif %}

{% if 'compilers_file' in spack %}
spack compilers:
  file.managed:
    - name: {{config_dir}}/compilers.yaml
    - template: jinja
    - defaults:
        mac_version: {{grains.get('mac_version', None)}}
        gccs: {{grains.get('gccs', {})}}
    - source: {{spack['compilers_file']}}
    - makedirs: True
{% endif %}

{% if 'external_packages' in spack %}
spack external packages:
  file.managed:
    - name: {{config_dir}}/packages.yaml
    - template: jinja
    - defaults:
        pythons: {{grains.get('pythons', {})}}
        cmakes: {{grains.get('cmakes', {})}}
        gits: {{grains.get('gits', {})}}
        pcres: {{grains.get('pcres', {})}}
    - source: {{spack['external_packages']}}
    - makedirs: True
{% endif %}

{% for name, url in spack.get('repos', {}).items() %}
spack repo {{name}}:
  spack.add_repo:
    - name: {{name}}
    - github: {{url}}
{% endfor %}

spack bootstrap:
  cmd.run:
    - name: |
        source $SPACK_ROOT/share/spack/setup-env.sh
        spack bootstrap
    - shell: /bin/sh
    - env:
        - SPACK_ROOT: {{directory}}

{% if spack.get('packages', None) != None %}
spack default packages:
  spack.installed:
    - pkgs: {{spack.get('packages')}}
{% endif %}

include:
  - .ipython
