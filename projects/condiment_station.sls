condiment_station:
    funwith.modulefile:
        - cwd: {{pillar['condiment_prefix']}}/black-garlic
        - prefix: {{pillar['condiment_prefix']}}
        - virtualenv: {{pillar['condiment_build_dir']}}/salt-env

UCL-RITS/CondimentStation:
  github.latest:
    - target: {{pillar['condiment_dir']}}
    - force_fetch: True
