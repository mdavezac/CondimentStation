{% set workspaces = salt['funwith.defaults']('workspaces') %}
{% set modulefiles = salt['funwith.defaults']('modulefiles') %}

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
