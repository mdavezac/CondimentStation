condiment_station:
    funwith.modulefile:
        - cwd: {{pillar['condiment_prefix']}}/black-garlic
        - prefix: {{pillar['condiment_prefix']}}
        - virtualenv: {{pillar['condiment_build_dir']}}/salt-env
        - footer: |
            set_alias("ispack", "spack python -c \"from IPython import embed; embed()\"")

UCL-RITS/CondimentStation:
  github.latest:
    - target: {{pillar['condiment_dir']}}
    - force_fetch: True
