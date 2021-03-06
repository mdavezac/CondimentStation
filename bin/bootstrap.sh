#! /bin/bash
set -e

prefix=$(pwd)
condiment_dir=$prefix/CondimentStation
virtenv=$prefix/build/salt-env
condiment_repo=git@github.com:UCL-RITS/CondimentStation.git
py=python2

mkdir -p $(pwd)/build

if [ ! -d "$virtenv" ]; then
  $py -m virtualenv $virtenv
  . $virtenv/bin/activate
  $py -m pip install --upgrade pip salt click GitPython mako pytest ipython virtualenv packaging
fi

if [[ "$(uname)" == "Darwin" ]] && [[ ! -e /usr/local/bin/brew ]]
then
   sudo chown -R $(whoami) /usr/local
   ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

if [[ ! -e "$condiment_dir/bin/pinch.py" ]] ; then
  git clone $condiment_repo
fi

$virtenv/bin/python $condiment_dir/bin/pinch.py setup server_hierarchy $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup syspath $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup minion $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup pillar $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup sync

if [[ -d "$prefix/black-garlic/.git" ]] ; then
  $virtenv/bin/python $condiment_dir/bin/pinch.py update
fi
