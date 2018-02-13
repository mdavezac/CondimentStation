{% set workspaces = salt['funwith.defaults']('workspaces') %}
{% set modulefiles = salt['funwith.defaults']('modulefiles') %}

lua:
  pkg.installed

{% if grains['os'] == "MacOS" %}
luarocks install luafilesystem:
  cmd.run:
    - unless: /usr/local/bin/lua -e 'require "lfs"'

luarocks install luaposix:
  cmd.run:
    - unless: /usr/local/bin/lua -e 'require "posix"'
{% else %}
funwith packages:
  pkg.installed:
    - pkgs: ['lua', 'lua-posix', 'lua-filesystem', 'lmod']
{% endif %}

{{workspaces}}:
  file.directory:
    - makedirs: True

{{modulefiles}}:
  file.directory:
    - makedirs: True
