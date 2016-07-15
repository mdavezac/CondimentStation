condiment_station:
    funwith.modulefile:
        - cwd: {{pillar['condiment_dir']}}/black-garlic
        - prefix: {{pillar['condiment_dir']}}
        - virtualenv:
            name: {{pillar['condiment_build_dir']}}/salt-env
