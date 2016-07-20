{% set condiments = salt['pillar.get']("condiments", {}) %}
{% set prefix = pillar["condiment_prefix"] %}
{% if condiments is mapping %}
{%   for subdir, condiment in condiments.items() %}
{%     if condiment is none %}
{{subdir}}:
  github.latest:
    - target: {{prefix}}/{{subdir}}
{%     else %}
{{subdir}} condiment:
{%       if 'git' in condiment %}
  git.latest:
    - name: {{condiment['git']}}
{%       else %}
  github.latest:
    - name: {{condiment.get('github', subdir)}}
{%       endif %}
    - target: {{prefix}}/{{subdir}}
{%       for key, value in condiment.items() %}
{%         if key not in ['name', 'github', 'git', 'target'] %}
    - {{key}}: {{value}}
{%         endif %}
{%       endfor %}
{%     endif %}
{%   endfor %}
{% else %}
{{condiments}}:
  github.latest:
    - target: {{prefix}}/{{condiments}}
{% endif %}
