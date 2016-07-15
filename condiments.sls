{% set condiments = salt['pillar.get']("condiments", {}) %}
{% set prefix = pillar["condiment_prefix"] %}
{% for subdir, condiment in condiments.items() %}
{{subdir}} condiment:
  file.directory:
    - name: {{prefix}}/{{subdir}}
    - makedirs: True
{%   if 'git' in condiment %}
  git.latest:
    - name: {{condiment['git']}}
{%   else %}
  github.latest:
    - name: {{condiment.get('github', subdir)}}
{%   endif %}
    - target: {{prefix}}/{{subdir}}
{%   for key, value in condiment.items() %}
{%       if key not in ['name', 'github', 'git', 'target'] %}
    - {{key}}: {{value}}
{%       endif %}
{%   endfor %}
{% endfor %}
