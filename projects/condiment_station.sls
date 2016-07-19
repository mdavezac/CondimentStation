condiment_station:
    funwith.modulefile:
        - cwd: {{pillar['condiment_dir']}}/black-garlic
        - prefix: {{pillar['condiment_prefix']}}
        - virtualenv: {{pillar['condiment_build_dir']}}/salt-env

mdavezac/CondimentStation:
  github.latest:
    - target: {{pillar['condiment_dir']}}
