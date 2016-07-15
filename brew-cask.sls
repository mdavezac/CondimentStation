brew-cask:
  cmd.wait:
    - order: 0
    - name: brew tap Caskroom/cask
    - creates: /usr/local/Library/Taps/caskroom/homebrew-cask
