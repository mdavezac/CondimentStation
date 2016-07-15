{{pillar['condiment_build_dir']}}/salt-env/share/scripts/spack_startup:
  file.managed:
    - makedirs: True
    - contents: |
        from os.path import join
        from sys import path
        spack_directory = "{{salt['spack.spack_directory']()}}"

        libdir = join(spack_directory, 'lib', 'spack')
        if libdir not in path:
            path.append(libdir)
            path.append(join(libdir, 'external'))

        import spack
        spack.debug = False
        spack.spack_working_dir = spack_directory

        import spack.cmd

{{pillar['condiment_build_dir']}}/salt-env/bin/ispack:
  file.managed:
    - contents: |
        PYTHONSTARTUP="{{pillar['condiment_build_dir']}}/salt-env/share/scripts/spack_startup" \
        {{pillar['condiment_build_dir']}}/salt-env/bin/python -m IPython $@
    - mode: 744

