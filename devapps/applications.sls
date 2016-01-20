development applications:
  pkg.installed:
    - pkgs:
      - cmake
      - ninja
      - hub
      - git
      - the_silver_searcher
      - pkg-config
      - clang-format
      - doxygen

universal-ctags:
  pkg.installed:
    - options:
      - --HEAD
    - taps: universal-ctags/universal-ctags

include:
  - .languages

vim:
  pkg.installed:
    - pkgs:
      - vim
      - macvim
    - options: ['--with-lua', '--with-luajit']
    - require:
        - pkg: languages
