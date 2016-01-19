{% set user = grains['user'] %}
{% set home = grains['userhome'] %}
{% set vimdir = salt['pillar.get']('vim:home', home + "/.vim") %}
{% set bundledir = salt['pillar.get']('vim:bundler_dir', vimdir + "/bundle") %}
{% set packages = salt['pillar.get']('vim:vundles', {}) %}
{% set method = 'present' %}
{% for package, stuff in packages.items() %}

{{package}}:
  github.{{method}}:
    - target: {{vimdir}}/{{package.split('/')[1]}}
{% if salt['pillar.get'](package + ":file", None) != None %}
  file.managed:
    - source: salt://files/vim/{{salt['pillar.get'](package + ":file")}}
    - target: {{bundledir}}/plugin/{{salt['pillar.get'](package + ":file")}}
{% elif salt['pillar.get'](package + ":text", None) != None %}
  file.managed:
    - contents: |
        {{salt['pillar.get'](package + ":text")}}
    - target: {{vimdir}}/plugin/{{package.split('/')[1]}}
{% endif %}
{% endfor %}
