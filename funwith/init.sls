{% set workspaces = salt['funwith.defaults']('workspaces') %}
{% set modulefiles = salt['funwith.defaults']('modulefiles') %}

lua:
  pkg.installed

luarocks install luafilesystem:
  cmd.run:
    - unless: /usr/local/bin/lua -e 'require "lfs"'

luarocks install luaposix:
  cmd.run:
    - unless: /usr/local/bin/lua -e 'require "posix"'

funwith:
  pkg.installed:
    - taps: homebrew/science
    - name: lmod

{{workspaces}}:
  file.directory:
    - makedirs: True

{{modulefiles}}:
  file.directory:
    - makedirs: True
