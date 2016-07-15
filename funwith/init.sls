{% set workspaces = salt['funwith.defaults']('workspaces') %}
{% set modulefiles = salt['funwith.defaults']('modulefiles') %}

funwith:
  pkg.installed:
    - taps: homebrew/science
    - name: lmod
    - require:
      - pkg: languages

{{workspaces}}:
  file.directory:
    - makedirs: True

{{modulefiles}}:
  file.directory:
    - makedirs: True
