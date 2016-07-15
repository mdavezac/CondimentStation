{% for script in ['pinch.py', 'setup.py'] %}
{{salt['pillar.get']('condiment_build_dir')}}/salt-env/bin/{{script}}:
  file.managed:
    - source: salt://CondimentStation/bin/{{script}}
    - mode: 744
    - template: jinja
    - defaults:
        condiment_dir: {{salt['pillar.get']('condiment_dir')}}
        condiment_prefix: {{salt['pillar.get']('condiment_prefix')}}
        condiment_python: {{salt['pillar.get']('condiment_python')}}
{% endfor %}
