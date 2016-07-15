condiment_station:
    funwith.modulefile:
        - cwd: {{pillar['condiment_dir']}}/blackgarlic
        - prefix: {{pillar['condiment_dir']}}
        - virtualenv:
            name: {{pillar['condiment_build_dir']}}/salt-env
