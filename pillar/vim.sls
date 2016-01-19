vim:
    home: {{grains['userhome']}}/.vim
    bundle_dir: {{grains['userhome']}}/.vim/bundle
    vundles:
        chrisbra/color_highlight:
